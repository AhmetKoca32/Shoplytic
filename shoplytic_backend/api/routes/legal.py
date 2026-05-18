from fastapi import APIRouter

from models.legal import LegalAnalysis, PetitionRequest
from agents.legal_agent import analyze_complaint, generate_petition

router = APIRouter()


@router.post("/analyze", response_model=LegalAnalysis)
async def analyze(body: dict):
    complaint = body.get("complaint", "")
    return await analyze_complaint(complaint)


@router.post("/petition")
async def petition(body: PetitionRequest):
    petition_text = await generate_petition(body)
    return {"petition_text": petition_text}
