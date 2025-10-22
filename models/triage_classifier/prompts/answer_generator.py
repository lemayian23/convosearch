from typing import List, Dict


class AnswerGenerator:
    def __init__(self):
        self.prompts = {
            "answer": """
            Based on the following context information, provide a concise and helpful answer to the user's question.

            User Question: {question}

            Relevant Context:
            {context}

            Instructions:
            - Be direct and helpful
            - Use only information from the context
            - If unsure, say you don't know
            - Keep response under 3 sentences

            Answer:
            """,

            "suggested_reply": """
            Based on the customer message and support context, generate a professional suggested reply.

            Customer Message: {message}

            Support Context:
            {context}

            Instructions:
            - Be empathetic and professional
            - Acknowledge the issue
            - Offer specific help based on context
            - Keep it under 2 sentences

            Suggested Reply:
            """
        }

    def generate_answer(self, question: str, context: List[str]) -> str:
        context_text = "\n".join([f"- {c}" for c in context])
        prompt = self.prompts["answer"].format(
            question=question,
            context=context_text
        )

        # For MVP, using simple template-based responses
        # In production, this would call an LLM API
        if any(word in question.lower() for word in ["password", "reset", "forgot"]):
            return "You can reset your password by clicking 'Forgot Password' on the login page and following the email instructions."
        elif any(word in question.lower() for word in ["billing", "invoice", "payment"]):
            return "Billing information and invoices are available in the Account Settings > Billing section of your dashboard."
        elif any(word in question.lower() for word in ["hours", "support", "available"]):
            return "Our support team is available Monday-Friday, 9AM-6PM EST."
        else:
            return "I understand you're looking for help. Our support team can assist you with this matter."

    def generate_suggested_reply(self, message: str, context: List[str]) -> str:
        context_text = "\n".join([f"- {c}" for c in context])
        prompt = self.prompts["suggested_reply"].format(
            message=message,
            context=context_text
        )

        # Simple template-based response for MVP
        if any(word in message.lower() for word in ["thank", "appreciate", "great"]):
            return "You're welcome! I'm glad I could help. Let us know if you need anything else."
        elif any(word in message.lower() for word in ["problem", "issue", "help"]):
            return "I understand you're experiencing an issue. I'll help you resolve this right away."
        else:
            return "Thank you for reaching out. I'll be happy to assist you with this."