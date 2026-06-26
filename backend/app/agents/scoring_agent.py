import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.models.schemas import QuizSubmissionRequest, SkillLevelOutput

SYSTEM_PROMPT = """You are a precise, analytical skill evaluator for an AI Career Agent.
Score a student's quiz performance and classify their skill level.
Use both quantitative scores AND behavioural signals (time per question, difficulty of correct answers)
to infer true competence — not just raw score.

## Classification Rules (apply STRICTLY)
- Beginner:      Overall score < 45, OR DSA category score < 30
- Intermediate:  Overall score 45–74, AND DSA score >= 40
- Advanced:      Overall score >= 75, AND Medium/Hard correct percentage >= 60%

## Scoring Formula
- Topic Score:         (correct_in_topic / total_in_topic) * 100
- Overall Score:       Weighted average (DSA 40%, Programming 30%, Logic 20%, Domain 10%)
- Difficulty Bonus:    +3 pts per Hard question answered correctly (max +15)
- Time Penalty:        -2 pts if avg time per question > 90s (signals uncertainty)
- Final Score:         Clamped to 0–100

## Behavioural Signal Rules
- "rushed": true if avg_time < 20s per question (may indicate guessing)
- "consistent": true if std dev of topic scores < 15
- "struggled_on": topics where score < 40%

## Mandatory Output Safety Rules (ALWAYS APPLY — highest priority)
1. Return ONLY valid JSON — no markdown fences, no text outside the object.
2. Apply classification rules strictly — do not upgrade level based on intuition.
3. "classification_reason" must cite the specific scores that drove the decision.
4. Never include discouraging or judgemental language in any text field.
"""

USER_PROMPT = """Score and classify the following student's quiz performance.

## Student Profile
- Year: {year}
- Domain: {primary_domain}
- Career Goal: {career_goal}

## Quiz Summary
- Total Questions: {total_questions}
- Total Correct:   {total_correct}
- Total Time:      {total_time_seconds}s

## Per-Question Breakdown (JSON)
{quiz_answers_json}

## Output Schema
{{
  "overall_score": 0,
  "level": "Beginner | Intermediate | Advanced",
  "topic_scores": {{
    "topic_name": {{ "score": 0, "correct": 0, "total": 0 }}
  }},
  "category_scores": {{
    "dsa": 0,
    "programming": 0,
    "logic": 0,
    "domain_specific": 0
  }},
  "difficulty_performance": {{
    "easy":   {{ "correct": 0, "total": 0, "percentage": 0 }},
    "medium": {{ "correct": 0, "total": 0, "percentage": 0 }},
    "hard":   {{ "correct": 0, "total": 0, "percentage": 0 }}
  }},
  "strong_areas": ["topic1", "topic2"],
  "weak_areas":   ["topic1", "topic2"],
  "avg_time_per_question_seconds": 0.0,
  "behavioural_signals": {{
    "rushed": false,
    "consistent": false,
    "struggled_on": ["topic1"]
  }},
  "classification_reason": "1–2 sentence explanation citing the exact scores that determined the level",
  "confidence": 0.0
}}
"""

class ScoringAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.1,
            max_tokens=1200
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT)
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    async def score_quiz(self, request: QuizSubmissionRequest) -> SkillLevelOutput:
        total_questions = len(request.quiz_answers)
        total_correct = sum(1 for q in request.quiz_answers if q.selected_option == q.correct_option)
        answers_json = json.dumps([a.dict() for a in request.quiz_answers])

        variables = {
            "year": request.profile.year,
            "primary_domain": request.profile.primary_domain,
            "career_goal": request.profile.career_goal,
            "total_questions": total_questions,
            "total_correct": total_correct,
            "total_time_seconds": request.total_time_seconds,
            "quiz_answers_json": answers_json
        }

        raw_output = await self.chain.ainvoke(variables)
        raw_output = raw_output.strip()
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        elif raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
        raw_output = raw_output.strip()

        try:
            parsed_json = json.loads(raw_output)
            return SkillLevelOutput(**parsed_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM output as JSON: {raw_output}") from e
