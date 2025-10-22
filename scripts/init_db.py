#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.ticket_manager import TicketManager

def main():
    print("Initializing database...")
    ticket_manager = TicketManager()
    ticket_manager.init_db()
    print("Database initialized successfully!")

if __name__ == "__main__":
    main()