from fastapi import APIRouter, HTTPException
from app.models.schemas import QuizGenerationRequest, QuizResponse
from app.agents.question_agent import QuestionAgent

router = APIRouter()
agent = QuestionAgent()

@router.post("/quiz/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizGenerationRequest):
    try:
        response = await agent.generate_quiz(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.models.schemas import QuizSubmissionRequest, SkillLevelOutput, SummaryGenerationRequest, ProfileSummaryOutput, RiskAssessmentRequest, RiskReportOutput
from app.agents.scoring_agent import ScoringAgent
from app.agents.summary_agent import SummaryAgent
from app.agents.risk_agent import RiskAgent

scoring_agent = ScoringAgent()
summary_agent = SummaryAgent()
risk_agent = RiskAgent()

@router.post("/quiz/submit", response_model=SkillLevelOutput)
async def submit_quiz(request: QuizSubmissionRequest):
    try:
        response = await scoring_agent.score_quiz(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile/summary", response_model=ProfileSummaryOutput)
async def generate_summary(request: SummaryGenerationRequest):
    try:
        response = await summary_agent.generate_summary(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile/risk", response_model=RiskReportOutput)
async def assess_risk(request: RiskAssessmentRequest):
    try:
        response = await risk_agent.assess_risk(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
