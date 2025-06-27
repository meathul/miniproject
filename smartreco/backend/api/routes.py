# Placeholder for FastAPI API routes

# Example:
# from fastapi import APIRouter
# router = APIRouter()
# ...

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from database.mongo import get_user_profile, store_user_profile
from agents.smartreco_agent import recommend_product

router = APIRouter()

class RecommendRequest(BaseModel):
    query: str
    user_id: str

class UpdateUserProfileRequest(BaseModel):
    user_id: str
    profile: dict

@router.post("/update_user")
async def update_user_profile_endpoint(req: UpdateUserProfileRequest):
    # Only allow certain fields
    allowed_fields = {"skin_type", "age", "ethnicity", "budget", "preferred_brands"}
    filtered_profile = {k: v for k, v in req.profile.items() if k in allowed_fields}
    store_user_profile(req.user_id, filtered_profile)
    return {"message": "User profile updated successfully."}

@router.post("/recommend")
async def recommend_endpoint(req: RecommendRequest):
    user_profile = get_user_profile(req.user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    result = recommend_product(req.query, user_profile)
    return result
