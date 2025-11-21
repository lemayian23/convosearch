ConvoSearch
RAG-powered Customer Support Insights & Auto-Ticket Triage

https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/python-3.9+-blue.svg
https://img.shields.io/badge/docker-ready-blue.svg

ConvoSearch is an intelligent customer support assistant that leverages Retrieval-Augmented Generation (RAG) to provide context-aware insights, automated ticket classification, and smart response suggestions. Streamline your support workflow with AI-powered document intelligence and automated triage.

🚀 Key Features
🔍 Document Intelligence
Smart Knowledge Base: Upload support documents, FAQs, and policy guides

Semantic Search: Query your knowledge base with natural language

Source Citations: Every response includes verifiable source references

Multi-format Support: Process PDFs, Word documents, text files, and more

🎯 Auto-Triage & Classification
Intelligent Routing: Automatically classify incoming customer messages into:

🤖 Bot: Simple queries that can be handled automatically

👨‍💼 Tier 1: Standard issues for support agents

⚡ Escalate: Complex issues requiring expert attention

Confidence Scoring: Get probability scores for each classification

Customizable Categories: Adapt classification to your support structure

💬 Smart Reply Generation
Context-Aware Responses: Generate suggested replies based on customer history and knowledge base

Tone Matching: Maintain consistent brand voice across responses

Multi-language Support: Generate responses in various languages

🎫 Ticket Management
Auto-Creation: Generate support tickets with pre-filled classification and context

Smart Pre-filling: Auto-populate priority, category, and suggested responses

Seamless Integration: Ready to connect with popular ticketing systems (Zendesk, Freshdesk, etc.)

🌐 Web Interface
Interactive Chat: Natural language interface for querying your knowledge base

Triage Dashboard: Visual overview of classification results and confidence scores

Ticket Creation: Streamlined workflow from chat to ticket creation

Responsive Design: Works seamlessly on desktop and mobile devices

🛠 Quick Start
Prerequisites
Docker & Docker Compose (Install Docker)

Python 3.9+ (for local development only)

4GB RAM minimum recommended

Installation & Running
bash
# Clone the repository
git clone <repository-url>
cd convosearch

# Build and run (recommended for first time)
make build
make run

# Or run in detached mode for background operation
make run-detached

# Run the demo to test the complete workflow
make demo
Alternative: Docker Commands
bash
# Build the containers
docker-compose build

# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f
📁 Project Structure
text
convosearch/
├── frontend/                 # React web interface
│   ├── src/
│   └── public/
├── backend/                  # FastAPI server
│   ├── app/
│   │   ├── models/          # Data models
│   │   ├── routes/          # API endpoints
│   │   └── services/        # Business logic
├── ml_services/              # ML and RAG services
│   ├── rag/                 # Document processing & retrieval
│   └── classification/      # Ticket triage models
├── docker-compose.yml       # Multi-container setup
└── Makefile                # Development utilities
🔧 Configuration
Environment Variables
Create a .env file in the root directory:

env
# API Keys (get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_URL=postgresql://user:password@db:5432/convosearch

# Application
DEBUG=false
LOG_LEVEL=INFO
First-Time Setup
Run make demo to initialize with sample data

Upload your support documents via the web interface

Configure your classification categories in the admin panel

Start processing customer queries!

🎯 Usage Examples
Querying Knowledge Base
python
# Example API call
response = client.query_knowledge_base(
    question="What is your refund policy?",
    context="customer inquiry about returns"
)
Auto-Triage Classification
python
classification = client.classify_ticket(
    message="I can't login to my account and need immediate help",
    customer_tier="premium"
)
# Returns: {"category": "escalate", "confidence": 0.92}
🚢 Deployment
Production Deployment
bash
# Build production images
make build-prod

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d
Cloud Deployment
AWS: ECS/EKS with RDS PostgreSQL

GCP: Cloud Run with Cloud SQL

Azure: Container Instances with Azure Database

🤝 Contributing
We welcome contributions! Please see our Contributing Guide for details.

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
📚 Documentation

🐛 Issue Tracker

💬 Discussions

📧 Email Support

🙏 Acknowledgments
Built with FastAPI and React

RAG powered by LangChain

ML models from Hugging Face

Vector embeddings with OpenAI