import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.models.schemas import SummaryGenerationRequest, ProfileSummaryOutput

SYSTEM_PROMPT = """You are an expert student profile analyst for an AI Career Agent serving Indian BTech CS students.
Your job is to synthesise all available student data into a clear, structured profile summary.
This summary will be used as shared context by downstream agents: RiskAgent, CareerRecommenderAgent,
and CourseRAGAgent.
Be concise, precise, and return ONLY a valid JSON object. No prose outside the JSON.

## Output Safety Rules
1. Return ONLY valid JSON — no markdown fences, no prose before or after.
2. Never fabricate details not present in the input — use null for missing fields.
3. If context is insufficient, set "insufficient_context": true on the relevant field.
4. Keep "summary_text" factual, encouraging, and free of negative judgements.
5. Never include offensive, discriminatory, or discouraging language.
"""

USER_PROMPT = """Generate a comprehensive student profile summary based on the following data.

## Student Profile
- Name: {student_name}
- Year: {year} (BTech CSE)
- Primary Domain: {primary_domain}
- Career Goal: {career_goal}

## Skill Assessment Results
- Overall Level: {level}
- Quiz Score: {total_score}/100
- DSA Score: {dsa_score}/100
- Programming Score: {programming_score}/100
- Logic Score: {logic_score}/100
- Strong Areas: {strong_areas}
- Weak Areas: {weak_areas}
- Avg Time per Question: {avg_time_seconds}s

## Output Schema
Return ONLY this JSON object:
{{
  "summary_text": "2–3 sentence natural language summary of the student",
  "skill_profile": {{
    "level": "Beginner | Intermediate | Advanced",
    "strengths": ["topic1", "topic2"],
    "gaps": ["topic1", "topic2"],
    "readiness_score": 0
  }},
  "focus_areas": ["area1", "area2", "area3"],
  "estimated_placement_readiness": "6 months | 12 months | 18 months | 24 months",
  "recommended_next_step": "Single most important action the student should take right now",
  "agent_context_tags": ["beginner", "placement", "ai-ml", "tier-2", "year-2"]
}}
"""

class SummaryAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            max_tokens=800
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT)
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    async def generate_summary(self, request: SummaryGenerationRequest) -> ProfileSummaryOutput:
        variables = {
            "student_name": request.profile.name,
            "year": request.profile.year,
            "primary_domain": request.profile.primary_domain,
            "career_goal": request.profile.career_goal,
            "level": request.skill_result.level,
            "total_score": request.skill_result.overall_score,
            "dsa_score": request.skill_result.category_scores.dsa,
            "programming_score": request.skill_result.category_scores.programming,
            "logic_score": request.skill_result.category_scores.logic,
            "strong_areas": ", ".join(request.skill_result.strong_areas),
            "weak_areas": ", ".join(request.skill_result.weak_areas),
            "avg_time_seconds": request.skill_result.avg_time_per_question_seconds
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
            return ProfileSummaryOutput(**parsed_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM output as JSON: {raw_output}") from e
