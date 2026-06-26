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
