import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.knowledge_base import DOCUMENTS

# ── What this file does ───────────────────────────────────────────────────────
# This is the RAG (Retrieval Augmented Generation) engine.
# RAG means: instead of letting an AI make up answers,
# we RETRIEVE relevant documents first, then GENERATE an answer
# grounded in those documents.
#
# Our RAG pipeline:
# 1. RETRIEVE: User asks a question → find the most relevant documents
# 2. AUGMENT: Add those documents as context to our answer
# 3. GENERATE: Build a response using only that context
#
# We use TF-IDF for retrieval because:
# - Works 100% offline — no API keys, no downloads
# - Fast — milliseconds to search
# - Explainable — easy to describe in interviews
# - Production-appropriate for focused knowledge bases

class RAGEngine:
    def __init__(self):
        self.documents = DOCUMENTS
        self.vectorizer = None
        self.tfidf_matrix = None
        self._build_index()

    def _build_index(self):
        """
        Builds the TF-IDF search index from our knowledge base.
        Called once when the engine starts up.

        TF-IDF converts each document into a vector of numbers.
        Documents with similar topics will have similar vectors.
        When a user asks a question, we convert the question to a vector
        and find the documents with the most similar vectors.
        """
        print("Building RAG search index...")

        # Combine title and content for better search coverage
        # The title is repeated twice to give it more weight
        texts = [
            f"{doc['title']} {doc['title']} {doc['content']}"
            for doc in self.documents
        ]

        # TfidfVectorizer settings:
        # max_features=3000 — keep the 3000 most important words
        # stop_words='english' — ignore words like "the", "and", "is"
        # ngram_range=(1,2) — match single words AND two-word phrases
        # e.g. "credit card" matches better than just "credit" or "card"
        self.vectorizer = TfidfVectorizer(
            max_features=3000,
            stop_words='english',
            ngram_range=(1, 2)
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        print(f"Index built: {len(self.documents)} documents indexed")

    def retrieve(self, query: str, top_k: int = 2):
        """
        Finds the most relevant documents for a given query.

        Steps:
        1. Convert query to TF-IDF vector
        2. Calculate cosine similarity with all document vectors
        3. Return top_k most similar documents

        Cosine similarity measures the angle between two vectors.
        Score of 1.0 = identical meaning
        Score of 0.0 = completely unrelated
        """
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(
            query_vector,
            self.tfidf_matrix
        ).flatten()

        # Get indices of top_k highest similarity scores
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            # Only include documents with meaningful relevance
            # Score below 0.05 means the document is probably not relevant
            if score > 0.05:
                results.append({
                    "document": self.documents[idx],
                    "relevance_score": round(score, 4)
                })

        return results

    def generate_answer(self, query: str, retrieved_docs: list) -> dict:
        """
        Generates a grounded answer from retrieved documents.

        This is the GENERATION step of RAG.
        We don't use an LLM here — we extract and structure relevant
        information directly from the retrieved documents.

        Why no LLM? Because:
        1. No hallucination risk — we only use what's in the documents
        2. No API costs — runs completely free
        3. Fully explainable — we can show exactly where each answer came from
        4. This is actually a valid production pattern for customer support
        """
        if not retrieved_docs:
            return {
                "answer": (
                    "I'm sorry, I couldn't find relevant information "
                    "for your question in our knowledge base. Please "
                    "contact our support team at support@ourcompany.com "
                    "or visit help.ourcompany.com for more help."
                ),
                "sources": [],
                "confidence": "low",
                "confidence_score": 0.0
            }

        # Build the answer from the most relevant document
        top_doc = retrieved_docs[0]
        top_score = top_doc["relevance_score"]

        # Determine confidence level based on relevance score
        # This is our faithfulness indicator — how well does the
        # retrieved content match the question?
        if top_score >= 0.15:
            confidence = "high"
        elif top_score >= 0.08:
            confidence = "medium"
        else:
            confidence = "low"

        # Build structured answer
        answer_parts = []

        # Add content from top document
        content = top_doc["document"]["content"].strip()
        answer_parts.append(content)

        # If we have a second relevant document, add relevant parts
        if len(retrieved_docs) > 1:
            second_doc = retrieved_docs[1]
            if second_doc["relevance_score"] >= 0.08:
                answer_parts.append(
                    f"\n\nAdditional information from "
                    f"'{second_doc['document']['title']}':\n"
                    f"{second_doc['document']['content'][:300].strip()}..."
                )

        answer = "\n\n".join(answer_parts)

        # Build source attribution — critical for RAG transparency
        sources = [
            {
                "title": doc["document"]["title"],
                "category": doc["document"]["category"],
                "relevance_score": doc["relevance_score"]
            }
            for doc in retrieved_docs
        ]

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "confidence_score": top_score
        }

    def ask(self, query: str) -> dict:
        """
        Main method — takes a question, retrieves relevant documents,
        and returns a grounded answer with source attribution.

        This is the full RAG pipeline in one method:
        Retrieve → Augment → Generate
        """
        retrieved = self.retrieve(query, top_k=2)
        result = self.generate_answer(query, retrieved)
        result["query"] = query
        result["num_sources_retrieved"] = len(retrieved)
        return result