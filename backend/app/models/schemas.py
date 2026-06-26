from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- Request Schemas ---

class StudentProfile(BaseModel):
    name: str = "Student"
    year: int = Field(..., ge=1, le=4, description="BTech CSE Year (1-4)")
    primary_domain: str = Field(..., description="Primary Domain Interest (e.g., AI/ML, Web Development)")
    career_goal: str = Field(..., description="Career Goal (e.g., Placement, Startup)")
    assumed_level: str = Field(..., description="Pre-quiz estimate based on year (Beginner, Intermediate, Advanced)")

class QuizGenerationRequest(BaseModel):
    profile: StudentProfile
    num_questions: int = Field(10, ge=5, le=20)
    easy_count: int = 3
    medium_count: int = 4
    hard_count: int = 3
    domain_specific_topics: str = "Relevant topics based on domain"

# --- Response Schemas ---

class QuestionOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class Question(BaseModel):
    question_id: str
    question_text: str
    options: QuestionOption
    correct_option: str
    explanation: str
    topic: str
    difficulty: str
    estimated_time_seconds: int

class QuizResponse(BaseModel):
    questions: List[Question]
