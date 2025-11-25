import psycopg2
import os
from datetime import datetime
from typing import Dict, Any

async def get_categories(self):
    """
    Retrieve distinct categories from the database
    """
    try:
        # Assuming you're using MongoDB
        categories = await self.collection.distinct("category")
        return [cat for cat in categories if cat]  # Filter out None values
        
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        return []


class TicketManager:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return self.conn

    def create_ticket(self, customer_message: str, classification: str, suggested_reply: str) -> Dict[str, Any]:
        """Create a new support ticket in the database"""
        conn = self.get_connection()
        cur = conn.cursor()

        try:
            ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

            cur.execute("""
                INSERT INTO tickets 
                (ticket_id, customer_message, classification, suggested_reply, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (ticket_id, customer_message, classification, suggested_reply, "open", datetime.now()))

            conn.commit()

            return {
                "ticket_id": ticket_id,
                "status": "created",
                "classification": classification
            }

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()

    def init_db(self):
        """Initialize the database schema"""
        conn = self.get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id SERIAL PRIMARY KEY,
                ticket_id VARCHAR(50) UNIQUE NOT NULL,
                customer_message TEXT NOT NULL,
                classification VARCHAR(20) NOT NULL,
                suggested_reply TEXT,
                status VARCHAR(20) DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP NULL
            )
        """)

        conn.commit()
        cur.close()