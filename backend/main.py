from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import random
from email_service import EmailService

app = FastAPI(title="B2B Lead Scraper API")

# Initialize email service
email_service = EmailService()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class LeadFilter(BaseModel):
    industry: str
    location: str
    limit: int = 50

class Lead(BaseModel):
    id: str
    business_name: str
    owner_name: str
    phone: str
    email: str
    address: str
    city: str
    state: str
    zip_code: str
    rating: float
    reviews: int
    website: Optional[str]
    verified: bool

class EmailCampaign(BaseModel):
    campaign_name: str
    template: str
    lead_ids: List[str]

# Sample data generator
def generate_sample_leads(count: int = 50):
    """Generate sample roofing business leads for demo"""
    roofing_companies = [
        "Elite Roofing Solutions", "Summit Roof Masters", "Premier Roofing Co",
        "Skyline Roofing Services", "Apex Roof Contractors", "Guardian Roofing LLC",
        "Heritage Roofing Group", "Precision Roofing Pros", "Dynasty Roofing Inc",
        "Victory Roofing Services", "Crown Roofing Company", "Liberty Roof Solutions"
    ]
    
    owner_names = [
        "John Smith", "Michael Johnson", "David Williams", "James Brown",
        "Robert Davis", "William Miller", "Richard Wilson", "Thomas Moore",
        "Charles Taylor", "Joseph Anderson", "Daniel White", "Matthew Harris"
    ]
    
    # Ensure lots of Texas cities for demo
    cities = [
        ("Houston", "TX"), ("Dallas", "TX"), ("Austin", "TX"), ("San Antonio", "TX"),
        ("Fort Worth", "TX"), ("El Paso", "TX"), ("Arlington", "TX"), ("Plano", "TX"),
        ("Phoenix", "AZ"), ("Atlanta", "GA"), ("Charlotte", "NC"), ("Jacksonville", "FL"),
        ("Nashville", "TN"), ("Denver", "CO"), ("Portland", "OR"), ("Las Vegas", "NV")
    ]
    
    leads = []
    # Generate exactly count number of leads
    for i in range(count):
        # Use modulo to cycle through cities when we have more leads than cities
        city_idx = i % len(cities)
        city, state = cities[city_idx]
        
        company_idx = i % len(roofing_companies)
        company = roofing_companies[company_idx]
        
        owner_idx = i % len(owner_names)
        owner = owner_names[owner_idx]
        
        lead = Lead(
            id=f"LEAD-{1000 + i}",
            business_name=f"{company} - {city}",
            owner_name=owner,
            phone=f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            email=f"{owner.lower().replace(' ', '.')}@{company.lower().replace(' ', '').replace('-', '')}.com",
            address=f"{random.randint(100, 9999)} Main Street",
            city=city,
            state=state,
            zip_code=f"{random.randint(10000, 99999)}",
            rating=round(random.uniform(3.5, 5.0), 1),
            reviews=random.randint(10, 500),
            website=f"www.{company.lower().replace(' ', '').replace('-', '')}.com",
            verified=random.choice([True, True, True, False])  # 75% verified
        )
        leads.append(lead)
    
    return leads

# In-memory storage for demo
demo_leads = generate_sample_leads(100)
campaigns = []

@app.get("/")
def root():
    return {
        "message": "B2B Lead Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "scrape": "/api/scrape",
            "leads": "/api/leads",
            "campaigns": "/api/campaigns",
            "stats": "/api/stats"
        }
    }

@app.post("/api/scrape")
async def scrape_leads(filters: LeadFilter):
    """
    Simulate scraping leads from Google Maps/Apify
    In production, this would call Apify API or Google Maps scraper
    """
    # Normalize location for matching
    location_lower = filters.location.lower().strip()
    
    # Filter leads by location (match state code, state name, or city)
    filtered_leads = []
    for lead in demo_leads:
        # Check if location matches state code, city, or if "texas" matches "TX"
        state_match = (
            location_lower == lead.state.lower() or  # Exact state code match
            location_lower in lead.city.lower() or   # City name match
            (location_lower == "texas" and lead.state == "TX") or  # Texas -> TX
            (location_lower == "arizona" and lead.state == "AZ") or
            (location_lower == "georgia" and lead.state == "GA") or
            (location_lower == "florida" and lead.state == "FL") or
            (location_lower == "tennessee" and lead.state == "TN") or
            (location_lower == "colorado" and lead.state == "CO") or
            (location_lower == "oregon" and lead.state == "OR") or
            (location_lower == "nevada" and lead.state == "NV") or
            (location_lower == "north carolina" and lead.state == "NC")
        )
        
        if state_match:
            filtered_leads.append(lead)
            if len(filtered_leads) >= filters.limit:
                break
    
    return {
        "status": "success",
        "scraping_source": "Google Maps + Apify",
        "industry": filters.industry,
        "location": filters.location,
        "total_found": len(filtered_leads),
        "leads": filtered_leads,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/leads")
def get_leads(limit: int = 50, verified_only: bool = False):
    """Get all scraped leads"""
    leads = demo_leads if not verified_only else [l for l in demo_leads if l.verified]
    return {
        "total": len(leads),
        "leads": leads[:limit]
    }

@app.post("/api/campaigns")
async def create_campaign(campaign: EmailCampaign):
    """Create an email campaign and send emails via local SMTP"""
    # Get leads for this campaign
    selected_leads = [lead for lead in demo_leads if lead.id in campaign.lead_ids]
    
    # Send emails using email service
    email_results = email_service.send_campaign(
        recipients=[{
            "email": lead.email,
            "business_name": lead.business_name,
            "owner_name": lead.owner_name,
            "city": lead.city,
            "state": lead.state,
            "rating": lead.rating
        } for lead in selected_leads],
        template=campaign.template
    )
    
    campaign_data = {
        "id": f"CAMP-{len(campaigns) + 1}",
        "name": campaign.campaign_name,
        "template": campaign.template,
        "lead_count": len(campaign.lead_ids),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "emails_sent": email_results["sent"],
        "emails_failed": email_results["failed"],
        "open_rate": 0,
        "response_rate": 0
    }
    campaigns.append(campaign_data)
    
    return {
        "status": "success",
        "message": f"Campaign created! {email_results['sent']} emails sent to MailHog",
        "campaign": campaign_data,
        "email_results": email_results
    }

@app.get("/api/campaigns")
def get_campaigns():
    """Get all email campaigns"""
    # Simulate some activity for demo
    for camp in campaigns:
        if camp["status"] == "scheduled":
            camp["status"] = "active"
            camp["emails_sent"] = random.randint(1, camp["lead_count"])
            camp["open_rate"] = round(random.uniform(15, 35), 1)
            camp["response_rate"] = round(random.uniform(2, 8), 1)
    
    return {
        "total": len(campaigns),
        "campaigns": campaigns
    }

@app.get("/api/stats")
def get_stats():
    """Get dashboard statistics"""
    total_leads = len(demo_leads)
    verified_leads = len([l for l in demo_leads if l.verified])
    
    return {
        "total_leads": total_leads,
        "verified_leads": verified_leads,
        "total_campaigns": len(campaigns),
        "active_campaigns": len([c for c in campaigns if c.get("status") == "active"]),
        "avg_rating": round(sum(l.rating for l in demo_leads) / total_leads, 2),
        "states_covered": len(set(l.state for l in demo_leads)),
        "data_sources": ["Google Maps API", "Apify", "Apollo.io"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
