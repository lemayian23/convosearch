#!/usr/bin/env python3
"""
ConvoSearch Demo Runner
This script sets up and demonstrates the complete MVP functionality.
"""
import os
import sys
import time
import requests
import json

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def wait_for_service(url, timeout=60):
    """Wait for a service to become available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(2)
    return False


def run_demo():
    print("🚀 Starting ConvoSearch Demo...")
    print("=" * 50)

    # Wait for services to be ready
    print("⏳ Waiting for services to start...")
    if not wait_for_service("http://localhost:8000/health"):
        print("❌ Services didn't start in time. Please check docker-compose logs.")
        return

    print("✅ Services are ready!")

    # Demo queries
    demo_queries = [
        "How do I reset my password?",
        "What are your business hours?",
        "How do I cancel my subscription?",
        "Where can I find my invoice?"
    ]

    # Demo messages for triage
    demo_messages = [
        "I forgot my password and can't login to my account",
        "There's a bug in the mobile app that makes it crash on startup",
        "I want to update my payment method for next billing",
        "The system is showing error messages when I try to export data"
    ]

    print("\n📚 Testing Knowledge Base Chat...")
    print("-" * 30)

    for query in demo_queries:
        print(f"\n🤔 Question: {query}")
        try:
            response = requests.post(
                "http://localhost:8000/api/query",
                json={"question": query, "collection": "faq"}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Answer: {data['answer']}")
                print(f"📎 Sources: {', '.join(data['sources'])}")
                print(f"🎯 Confidence: {data['confidence']:.2f}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Request failed: {e}")

    print("\n🚨 Testing Auto-Triage System...")
    print("-" * 30)

    for message in demo_messages:
        print(f"\n📨 Message: {message}")
        try:
            response = requests.post(
                "http://localhost:8000/api/triage",
                json={"message": message}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"🏷️ Classification: {data['classification']} (confidence: {data['confidence']:.2f})")
                print(f"💡 Suggested Reply: {data['suggested_reply']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Request failed: {e}")

    print("\n🎫 Testing Ticket Creation...")
    print("-" * 30)

    # Create a sample ticket
    sample_message = "I need help with billing and invoice access"
    try:
        # First triage the message
        triage_response = requests.post(
            "http://localhost:8000/api/triage",
            json={"message": sample_message}
        )

        if triage_response.status_code == 200:
            triage_data = triage_response.json()

            # Then create a ticket
            ticket_response = requests.post(
                "http://localhost:8000/api/tickets",
                json={
                    "customer_message": sample_message,
                    "classification": triage_data["classification"],
                    "suggested_reply": triage_data["suggested_reply"]
                }
            )

            if ticket_response.status_code == 200:
                ticket_data = ticket_response.json()
                print(f"✅ Ticket created: {ticket_data['ticket_id']}")

                # List recent tickets
                tickets_response = requests.get("http://localhost:8000/api/tickets")
                if tickets_response.status_code == 200:
                    tickets_data = tickets_response.json()
                    print(f"📋 Total tickets in system: {len(tickets_data['tickets'])}")
            else:
                print(f"❌ Ticket creation failed: {ticket_response.status_code}")
    except Exception as e:
        print(f"❌ Ticket test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 Demo completed successfully!")
    print("\n🌐 Access the web interface at: http://localhost:8000")
    print("🔍 Knowledge Base Chat: http://localhost:8000/chat")
    print("🚨 Message Triage: http://localhost:8000/triage")
    print("📋 Tickets API: http://localhost:8000/api/tickets")
    print("\n💡 Try the web interface for the full interactive experience!")


if __name__ == "__main__":
    run_demo()