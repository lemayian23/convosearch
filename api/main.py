from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import sys

# Add these imports at the top if not already present
from datetime import datetime
from typing import Optional, List

# Update your existing search endpoint or add a new one
@app.post("/api/search")
async def search_queries(
    query: str = Body(..., embed=True),
    category_filter: Optional[str] = Body(None),
    date_filter: Optional[str] = Body(None),
    limit: int = Body(10)
):
    """
    Search queries with filtering options
    """
    try:
        # Build filter criteria
        filter_criteria = {}
        
        if category_filter and category_filter != "all":
            filter_criteria["category"] = category_filter
            
        if date_filter and date_filter != "all":
            # Handle different date filter options
            if date_filter == "today":
                start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                filter_criteria["date_from"] = start_date
            elif date_filter == "week":
                start_date = datetime.now() - timedelta(days=7)
                filter_criteria["date_from"] = start_date
            elif date_filter == "month":
                start_date = datetime.now() - timedelta(days=30)
                filter_criteria["date_from"] = start_date
            # Add more date filters as needed
        
        # Use your existing RAG engine with filters
        results = await rag_engine.search(
            query=query,
            filter_criteria=filter_criteria,
            limit=limit
        )
        
        return {
            "success": True,
            "results": results,
            "query": query,
            "filters": {
                "category": category_filter,
                "date": date_filter
            }
        }
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "results": []
        }

@app.get("/api/categories")
async def get_categories():
    """
    Get available categories for filtering
    """
    try:
        # This should query your database for distinct categories
        categories = await ticket_manager.get_categories()
        return {
            "success": True,
            "categories": categories
        }
    except Exception as e:
        logger.error(f"Categories error: {str(e)}")
        return {
            "success": False,
            "categories": [],
            "error": str(e)
        }

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.rag_engine import RAGEngine
from api.ticket_manager import TicketManager
from models.triage_classifier.classifier import TriageClassifier
from models.prompts.answer_generator import AnswerGenerator
from ingestion.parser import DocumentParser
from ingestion.embedder import EmbeddingGenerator

app = FastAPI(title="ConvoSearch API", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="webui/static"), name="static")
templates = Jinja2Templates(directory="webui/templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
rag_engine = RAGEngine()
ticket_manager = TicketManager()
triage_classifier = TriageClassifier()
answer_generator = AnswerGenerator()
document_parser = DocumentParser()
embedding_generator = EmbeddingGenerator()


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    ticket_manager.init_db()
    print("ConvoSearch API started successfully!")


# Request/Response models
class QueryRequest(BaseModel):
    question: str
    collection: str = "faq"


class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float


class TriageRequest(BaseModel):
    message: str


class TriageResponse(BaseModel):
    classification: str  # "bot", "tier1", "escalate"
    confidence: float
    suggested_reply: str
    sources: List[str]


class TicketCreateRequest(BaseModel):
    customer_message: str
    classification: str
    suggested_reply: str


class TicketCreateResponse(BaseModel):
    ticket_id: str
    status: str


class UploadResponse(BaseModel):
    filename: str
    status: str
    chunks_processed: int


# Web UI Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/triage", response_class=HTMLResponse)
async def triage_interface(request: Request):
    return templates.TemplateResponse("triage.html", {"request": request})


# API Routes
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ConvoSearch API"}


@app.post("/api/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base for answers"""
    try:
        # Get relevant context from RAG engine
        context = rag_engine.get_relevant_context(request.question)

        # Generate answer using the context
        answer = answer_generator.generate_answer(request.question, context)

        # Get source information
        rag_results = rag_engine.query(request.question, request.collection)
        sources = [source["source"] for source in rag_results["sources"][:2]]  # Top 2 sources

        return QueryResponse(
            answer=answer,
            sources=sources if sources else ["general_knowledge"],
            confidence=rag_results["average_confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/api/triage", response_model=TriageResponse)
async def triage_message(request: TriageRequest):
    """Classify and triage incoming customer message"""
    try:
        # Classify the message
        classification_result = triage_classifier.classify(request.message)

        # Get relevant context for suggested reply
        context = rag_engine.get_relevant_context(request.message, ["faq", "tickets"])

        # Generate suggested reply
        suggested_reply = answer_generator.generate_suggested_reply(request.message, context)

        return TriageResponse(
            classification=classification_result["classification"],
            confidence=classification_result["confidence"],
            suggested_reply=suggested_reply,
            sources=[f"{classification_result['classification']}_category"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Triage failed: {str(e)}")


@app.post("/api/tickets", response_model=TicketCreateResponse)
async def create_ticket(request: TicketCreateRequest):
    """Create a new support ticket"""
    try:
        result = ticket_manager.create_ticket(
            request.customer_message,
            request.classification,
            request.suggested_reply
        )

        return TicketCreateResponse(
            ticket_id=result["ticket_id"],
            status=result["status"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ticket creation failed: {str(e)}")


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')

        # Parse document into chunks
        chunks = document_parser.parse_text(text_content, doc_type=file.filename.split('.')[-1])

        # Generate embeddings and store in vector DB
        await embedding_generator.generate_embeddings(chunks, collection_name="uploaded_docs")

        return UploadResponse(
            filename=file.filename,
            status="processed",
            chunks_processed=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/api/tickets")
async def list_tickets():
    """List all tickets (for demo purposes)"""
    try:
        conn = ticket_manager.get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT ticket_id, customer_message, classification, suggested_reply, status, created_at
            FROM tickets ORDER BY created_at DESC LIMIT 10
        """)

        tickets = []
        for row in cur.fetchall():
            tickets.append({
                "ticket_id": row[0],
                "customer_message": row[1],
                "classification": row[2],
                "suggested_reply": row[3],
                "status": row[4],
                "created_at": row[5].isoformat() if row[5] else None
            })

        cur.close()
        return {"tickets": tickets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickets: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)