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

# --- Scoring Agent Schemas ---
class QuizAnswer(BaseModel):
    question_id: str
    question_text: str
    selected_option: str
    correct_option: str
    topic: str
    difficulty: str
    time_taken_seconds: int

class QuizSubmissionRequest(BaseModel):
    student_id: str
    session_id: str
    profile: StudentProfile
    quiz_answers: List[QuizAnswer]
    total_time_seconds: int

class TopicScore(BaseModel):
    score: int
    correct: int
    total: int

class CategoryScores(BaseModel):
    dsa: int
    programming: int
    logic: int
    domain_specific: int

class DifficultyStats(BaseModel):
    correct: int
    total: int
    percentage: int

class DifficultyPerformance(BaseModel):
    easy: DifficultyStats
    medium: DifficultyStats
    hard: DifficultyStats

class BehaviouralSignals(BaseModel):
    rushed: bool
    consistent: bool
    struggled_on: List[str]

class SkillLevelOutput(BaseModel):
    overall_score: int
    level: str
    topic_scores: Dict[str, TopicScore]
    category_scores: CategoryScores
    difficulty_performance: DifficultyPerformance
    strong_areas: List[str]
    weak_areas: List[str]
    avg_time_per_question_seconds: float
    behavioural_signals: BehaviouralSignals
    classification_reason: str
    confidence: float

# --- Summary Agent Schemas ---
class SummarySkillProfile(BaseModel):
    level: str
    strengths: List[str]
    gaps: List[str]
    readiness_score: int

class ProfileSummaryOutput(BaseModel):
    summary_text: str
    skill_profile: SummarySkillProfile
    focus_areas: List[str]
    estimated_placement_readiness: str
    recommended_next_step: str
    agent_context_tags: List[str]

class SummaryGenerationRequest(BaseModel):
    profile: StudentProfile
    skill_result: SkillLevelOutput

# --- Risk Agent Schemas ---
class TimelineRisk(BaseModel):
    level: str
    reason: str
    months_needed: int
    months_available: int
    is_achievable: bool

class SkillGap(BaseModel):
    area: str
    severity: str
    description: str
    fix_timeline_weeks: int
    priority: int

class StrategicRisk(BaseModel):
    risk: str
    impact: str
    mitigation: str

class RiskReportOutput(BaseModel):
    overall_risk_level: str
    timeline_risk: TimelineRisk
    skill_gaps: List[SkillGap]
    strategic_risks: List[StrategicRisk]
    quick_wins: List[str]
    red_flags: List[str]
    risk_summary: str

class RiskAssessmentRequest(BaseModel):
    profile: StudentProfile
    summary: ProfileSummaryOutput
    years_remaining: float
    hours_per_day: int
