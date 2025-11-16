import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Service, Project, Testimonial, Inquiry

app = FastAPI(title="ServiceMedia Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ServiceMedia Clone API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"
    return response

# Content endpoints
@app.get("/api/services", response_model=List[Service])
def list_services():
    docs = get_documents("service", {})
    # transform _id out
    return [Service(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.get("/api/projects", response_model=List[Project])
def list_projects():
    docs = get_documents("project", {})
    return [Project(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials():
    docs = get_documents("testimonial", {})
    return [Testimonial(**{k: v for k, v in d.items() if k != "_id"}) for d in docs]

class InquiryResponse(BaseModel):
    status: str

@app.post("/api/inquiry", response_model=InquiryResponse)
def create_inquiry(payload: Inquiry):
    try:
        create_document("inquiry", payload)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: simple seeding route for demo
@app.post("/api/seed")
def seed():
    try:
        # Seed only if empty
        if db["service"].count_documents({}) == 0:
            sample_services = [
                {"title": "Digital Marketing", "slug": "digital-marketing", "short": "Growth-focused campaigns", "description": "Performance marketing across search, social, and programmatic.", "icon": "rocket", "featured": True},
                {"title": "Brand Strategy", "slug": "brand-strategy", "short": "Positioning that resonates", "description": "Identity systems, voice, and messaging for modern brands.", "icon": "sparkles", "featured": True},
                {"title": "Web Experiences", "slug": "web-experiences", "short": "High-velocity websites", "description": "Conversion-optimized, fast, and accessible frontends.", "icon": "globe-2", "featured": True},
                {"title": "Video Production", "slug": "video-production", "short": "Stories that move", "description": "End-to-end creative, production, and post.", "icon": "video", "featured": False}
            ]
            for s in sample_services:
                create_document("service", s)
        if db["project"].count_documents({}) == 0:
            sample_projects = [
                {"title": "NeoFin App Launch", "slug": "neofin-app", "summary": "Full-funnel launch with 2.3x ROI", "image": "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?q=80&w=1200&auto=format&fit=crop", "tags": ["performance", "mobile"], "link": None, "featured": True},
                {"title": "Aether Commerce", "slug": "aether-commerce", "summary": "Headless storefront with 98 Lighthouse", "image": "https://images.unsplash.com/photo-1509395176047-4a66953fd231?q=80&w=1200&auto=format&fit=crop", "tags": ["web", "headless"], "link": None, "featured": True}
            ]
            for p in sample_projects:
                create_document("project", p)
        if db["testimonial"].count_documents({}) == 0:
            sample_testimonials = [
                {"author": "Priya Sharma", "role": "CMO, Aether", "quote": "They delivered beyond expectations — creative, fast, and data-driven.", "company": "Aether", "avatar": None, "featured": True},
                {"author": "Rahul Mehta", "role": "Founder, NeoFin", "quote": "Our growth engine started the week we onboarded them.", "company": "NeoFin", "avatar": None, "featured": True}
            ]
            for t in sample_testimonials:
                create_document("testimonial", t)
        return {"status": "seeded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
