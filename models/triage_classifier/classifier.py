import numpy as np
from typing import Dict, Any
import json
import os


class TriageClassifier:
    def __init__(self):
        # Simple rule-based classifier for MVP
        # In production, this would be a fine-tuned transformer model
        self.rules = {
            "bot": [
                "password reset", "forgot password", "business hours",
                "cancel subscription", "where is", "how to", "what is"
            ],
            "tier1": [
                "billing", "payment", "invoice", "account", "subscription",
                "refund", "cancel", "update"
            ],
            "escalate": [
                "bug", "crash", "error", "not working", "broken",
                "emergency", "urgent", "critical"
            ]
        }

    def classify(self, message: str) -> Dict[str, Any]:
        message_lower = message.lower()

        scores = {"bot": 0, "tier1": 0, "escalate": 0}

        for category, keywords in self.rules.items():
            for keyword in keywords:
                if keyword in message_lower:
                    scores[category] += 1

        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            for category in scores:
                scores[category] = scores[category] / total

        # Determine classification
        if total == 0:
            classification = "tier1"  # Default fallback
            confidence = 0.5
        else:
            classification = max(scores.items(), key=lambda x: x[1])
            confidence = classification[1]
            classification = classification[0]

        return {
            "classification": classification,
            "confidence": confidence,
            "scores": scores
        }