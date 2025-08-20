from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from pymongo import MongoClient
import uuid
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(title="DSC Team Management API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "dsc_club")

# MongoDB client
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
members_collection = db.team_members

# Pydantic models
class TeamMember(BaseModel):
    name: str
    role: str
    photo: Optional[str] = None
    description: Optional[str] = None

class TeamMemberResponse(BaseModel):
    id: str
    name: str
    role: str
    photo: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    photo: Optional[str] = None
    description: Optional[str] = None

# API Routes

@app.get("/")
async def root():
    return {"message": "DSC Team Management API", "status": "running"}

@app.get("/api/health")
async def health_check():
    try:
        # Test database connection
        client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/api/team-members", response_model=TeamMemberResponse)
async def create_team_member(member: TeamMember):
    try:
        # Generate unique ID
        member_id = str(uuid.uuid4())
        current_time = datetime.utcnow()
        
        # Create member document
        member_doc = {
            "id": member_id,
            "name": member.name,
            "role": member.role,
            "photo": member.photo,
            "description": member.description,
            "created_at": current_time,
            "updated_at": current_time
        }
        
        # Insert into database
        result = members_collection.insert_one(member_doc)
        
        if result.inserted_id:
            return TeamMemberResponse(**member_doc)
        else:
            raise HTTPException(status_code=500, detail="Failed to create team member")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating team member: {str(e)}")

@app.get("/api/team-members", response_model=List[TeamMemberResponse])
async def get_team_members():
    try:
        # Fetch all team members
        members = list(members_collection.find({}, {"_id": 0}).sort("created_at", 1))
        return [TeamMemberResponse(**member) for member in members]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching team members: {str(e)}")

@app.get("/api/team-members/{member_id}", response_model=TeamMemberResponse)
async def get_team_member(member_id: str):
    try:
        member = members_collection.find_one({"id": member_id}, {"_id": 0})
        if not member:
            raise HTTPException(status_code=404, detail="Team member not found")
        return TeamMemberResponse(**member)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching team member: {str(e)}")

@app.put("/api/team-members/{member_id}", response_model=TeamMemberResponse)
async def update_team_member(member_id: str, member_update: TeamMemberUpdate):
    try:
        # Check if member exists
        existing_member = members_collection.find_one({"id": member_id}, {"_id": 0})
        if not existing_member:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Prepare update data
        update_data = {}
        if member_update.name is not None:
            update_data["name"] = member_update.name
        if member_update.role is not None:
            update_data["role"] = member_update.role
        if member_update.photo is not None:
            update_data["photo"] = member_update.photo
        if member_update.description is not None:
            update_data["description"] = member_update.description
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Update in database
        result = members_collection.update_one(
            {"id": member_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made to team member")
        
        # Fetch updated member
        updated_member = members_collection.find_one({"id": member_id}, {"_id": 0})
        return TeamMemberResponse(**updated_member)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating team member: {str(e)}")

@app.delete("/api/team-members/{member_id}")
async def delete_team_member(member_id: str):
    try:
        # Check if member exists
        existing_member = members_collection.find_one({"id": member_id})
        if not existing_member:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        # Delete from database
        result = members_collection.delete_one({"id": member_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete team member")
        
        return {"message": "Team member deleted successfully", "id": member_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting team member: {str(e)}")

# Additional endpoints for club information
@app.get("/api/club-info")
async def get_club_info():
    return {
        "name": "Developer Students Club",
        "institute": "SRM Institute of Science and Technology",
        "campus": "Ramapuram",
        "description": "Empowering the next generation of developers through collaborative learning, innovative projects, and community building.",
        "mission": "Developer Students Club at SRM IST Ramapuram is a community-driven initiative that aims to help students bridge the gap between theory and practice.",
        "activities": [
            "Workshops and technical sessions",
            "Hackathons and coding competitions",
            "Study jams and collaborative learning",
            "Open-source contributions",
            "Industry mentorship programs"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)