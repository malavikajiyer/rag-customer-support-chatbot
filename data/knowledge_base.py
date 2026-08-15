# ── Knowledge Base ────────────────────────────────────────────────────────────
# This is the document collection our chatbot uses to answer questions.
# In a real company this would be loaded from a database or document store.
# We're using a tech company FAQ as our example — clear, realistic, and
# something every interviewer immediately understands.
#
# Each document has:
# - id: unique identifier
# - category: topic area
# - title: what this document is about
# - content: the actual text the RAG system searches through

DOCUMENTS = [
    {
        "id": "1",
        "category": "pricing",
        "title": "Pricing Plans",
        "content": """We offer three pricing plans:
        
        Starter Plan: £29 per month. Includes up to 5 users, 10GB storage, 
        email support, and access to all basic features. Perfect for small teams.
        
        Professional Plan: £79 per month. Includes up to 25 users, 100GB storage, 
        priority email and chat support, advanced analytics, and API access. 
        Most popular for growing businesses.
        
        Enterprise Plan: Custom pricing. Includes unlimited users, unlimited storage, 
        24/7 dedicated support, custom integrations, SLA guarantee, and a dedicated 
        account manager. Contact our sales team for a quote."""
    },
    {
        "id": "2",
        "category": "billing",
        "title": "Billing and Payments",
        "content": """Billing questions answered:
        
        Payment methods: We accept all major credit cards (Visa, Mastercard, Amex), 
        PayPal, and bank transfer for annual plans.
        
        Billing cycle: Monthly plans are billed on the same date each month. 
        Annual plans are billed once per year and receive a 20% discount.
        
        Invoices: Invoices are automatically emailed to your billing email address 
        on each billing date. You can also download past invoices from your account dashboard.
        
        Failed payments: If a payment fails we will retry after 3 days and 7 days. 
        After three failed attempts your account will be suspended until payment is resolved.
        
        Refunds: We offer a 30-day money back guarantee for new customers. 
        Refunds are processed within 5-10 business days."""
    },
    {
        "id": "3",
        "category": "account",
        "title": "Account Management",
        "content": """Managing your account:
        
        Password reset: Click Forgot Password on the login page. You will receive 
        a reset link within 5 minutes. Check your spam folder if it does not arrive.
        
        Changing email: Go to Settings > Profile > Email Address. You will need to 
        verify your new email address before the change takes effect.
        
        Two factor authentication: We strongly recommend enabling 2FA. Go to 
        Settings > Security > Two Factor Authentication. We support authenticator 
        apps and SMS verification.
        
        Deleting your account: Go to Settings > Account > Delete Account. 
        Please note this action is permanent and all your data will be deleted 
        within 30 days. Download your data before deleting."""
    },
    {
        "id": "4",
        "category": "technical",
        "title": "Technical Support and Troubleshooting",
        "content": """Common technical issues and solutions:
        
        Login problems: Clear your browser cache and cookies. Try a different browser. 
        Make sure caps lock is not on. If you still cannot log in contact support.
        
        Slow performance: Check your internet connection. Try refreshing the page. 
        Clear browser cache. If the problem persists check our status page at 
        status.ourcompany.com for any ongoing incidents.
        
        Data not syncing: Log out and log back in. Check you have a stable internet 
        connection. If data is still not syncing after 10 minutes contact support 
        with your account email and a description of the issue.
        
        Browser compatibility: We support the latest versions of Chrome, Firefox, 
        Safari, and Edge. Internet Explorer is not supported.
        
        Mobile app: Our mobile app is available on iOS and Android. 
        Make sure you have the latest version installed."""
    },
    {
        "id": "5",
        "category": "features",
        "title": "Product Features",
        "content": """Key product features:
        
        Dashboard: Get a real-time overview of all your key metrics in one place. 
        Customise your dashboard by adding and removing widgets.
        
        Reports: Generate automated reports on a daily, weekly, or monthly basis. 
        Export reports as PDF, CSV, or Excel. Schedule reports to be emailed to 
        your team automatically.
        
        Integrations: We integrate with over 50 popular tools including Slack, 
        Microsoft Teams, Salesforce, HubSpot, Zapier, and Google Workspace. 
        Find the full list in our integrations marketplace.
        
        API: Our REST API allows you to build custom integrations. 
        Full API documentation is available at docs.ourcompany.com. 
        API access is included in Professional and Enterprise plans."""
    },
    {
        "id": "6",
        "category": "security",
        "title": "Security and Data Privacy",
        "content": """Security and privacy information:
        
        Data encryption: All data is encrypted at rest using AES-256 and in 
        transit using TLS 1.3. We never store plain text passwords.
        
        GDPR compliance: We are fully GDPR compliant. You can request a copy of 
        your data or request deletion at any time by contacting privacy@ourcompany.com.
        
        Data location: All data is stored in UK and EU data centres. 
        We do not transfer data outside the UK or EU without explicit consent.
        
        Security certifications: We are ISO 27001 certified and undergo annual 
        third-party security audits. Our last audit was completed in January 2026.
        
        Reporting vulnerabilities: If you discover a security vulnerability please 
        email security@ourcompany.com. We have a responsible disclosure policy."""
    },
    {
        "id": "7",
        "category": "getting_started",
        "title": "Getting Started Guide",
        "content": """How to get started:
        
        Step 1 - Sign up: Create your account at ourcompany.com/signup. 
        You can start with a free 14-day trial, no credit card required.
        
        Step 2 - Set up your workspace: Add your company name, logo, and 
        invite your team members via email.
        
        Step 3 - Import your data: Use our import wizard to bring in data 
        from CSV files or connect your existing tools via integrations.
        
        Step 4 - Explore the dashboard: Take our interactive product tour 
        to learn the key features. The tour takes about 10 minutes.
        
        Step 5 - Get help: Our help centre at help.ourcompany.com has 
        over 200 articles. You can also contact support via live chat 
        Monday to Friday 9am to 6pm UK time."""
    },
    {
        "id": "8",
        "category": "cancellation",
        "title": "Cancellation Policy",
        "content": """Cancellation information:
        
        How to cancel: Go to Settings > Billing > Cancel Subscription. 
        You can cancel at any time with no cancellation fees.
        
        What happens after cancellation: You will retain access to your account 
        until the end of your current billing period. After that your account 
        will be downgraded to a read-only state for 30 days so you can export 
        your data.
        
        Data after cancellation: Your data is kept for 90 days after cancellation 
        in case you decide to reactivate. After 90 days all data is permanently deleted.
        
        Reactivation: You can reactivate your account at any time within 90 days 
        of cancellation. All your data will be restored. Contact support to reactivate."""
    }
]