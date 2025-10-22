# ConvoSearch
RAG-powered Customer Support Insights & Auto-Ticket Triage

## 🚀 MVP Features
- **Document Intelligence**: Upload and query knowledge base with source citations
- **Auto-Triage**: Classify customer messages (bot/tier1/escalate) with confidence scoring
- **Smart Replies**: Generate context-aware suggested responses
- **Ticket Management**: Create tickets with pre-filled classification and replies
- **Web Interface**: Full-featured UI for chat, triage, and ticket creation

## 🛠 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for local development)

### Installation & Running
```bash
# Clone and setup
git clone <repository>
cd convosearch

# Build and run (recommended for first time)
make build
make run

# Or run in detached mode
make run-detached

# Run the demo to test everything
make demo