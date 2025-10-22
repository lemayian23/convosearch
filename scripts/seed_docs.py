#!/usr/bin/env python3
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.parser import DocumentParser
from ingestion.embedder import EmbeddingGenerator
import asyncio


async def main():
    print("Seeding sample documents...")

    # Sample FAQ content
    faq_content = """
    Q: How do I reset my password?
    A: Click 'Forgot Password' on the login page and follow the email instructions.

    Q: What are your business hours?
    A: Our support team is available Monday-Friday, 9AM-6PM EST.

    Q: How do I cancel my subscription?
    A: Go to Account Settings > Billing > Cancel Subscription.

    Q: Where can I find my invoice?
    A: Invoices are available in the Billing section of your account dashboard.

    Q: Do you offer refunds?
    A: We offer 30-day money-back guarantee for annual plans.
    """

    # Sample ticket content
    tickets_content = """
    Ticket #001: User cannot login - reset password not working. Customer tried resetting password but not receiving email. Issue: email delivery delay.
    Ticket #002: Billing question - user wants to change payment method. Assisted with updating credit card information.
    Ticket #003: Feature request - dark mode. Explained this is on roadmap for Q2.
    Ticket #004: Bug report - mobile app crashing on iOS. Collected device details and escalated to engineering.
    Ticket #005: Account deletion request. Guided user through account settings and confirmed deletion.
    """

    parser = DocumentParser()
    embedder = EmbeddingGenerator()

    # Parse and embed FAQ
    faq_chunks = parser.parse_text(faq_content, doc_type="faq")
    await embedder.generate_embeddings(faq_chunks, collection_name="faq")

    # Parse and embed tickets
    ticket_chunks = parser.parse_text(tickets_content, doc_type="tickets")
    await embedder.generate_embeddings(ticket_chunks, collection_name="tickets")

    print("Sample documents seeded successfully!")


if __name__ == "__main__":
    asyncio.run(main())