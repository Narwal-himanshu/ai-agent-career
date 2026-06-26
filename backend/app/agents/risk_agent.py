import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.models.schemas import RiskAssessmentRequest, RiskReportOutput

SYSTEM_PROMPT = """You are a career risk analyst for Indian BTech CS students.
Your role is to identify skill gaps, timeline risks, and strategic misalignments between a
student's current profile and their stated career goal.
Be realistic, constructive, and specific to the Indian tech ecosystem
(FAANG/MNCs, product startups, GATE, research labs, higher studies).
Prioritise actionable risks — things the student can actually fix — over systemic ones.
Return ONLY valid JSON. No prose outside the JSON object.

## Output Safety Rules
1. Return ONLY valid JSON — no markdown fences, no explanatory text outside the object.
2. Be constructive, not discouraging — frame risks as opportunities to act.
3. Never include personal judgements about intelligence, ability, or background.
4. "quick_wins" must be specific and achievable within 1–2 weeks.
5. If context is insufficient, set the affected field to null.
"""

USER_PROMPT = """Perform a comprehensive risk assessment for the following student.

## Student Summary
{student_summary_json}

## Career Goal Details
- Primary Goal: {career_goal}
- Target Timeline: {years_remaining} years remaining in college
- Domain: {primary_domain}
- Hours Available/Day: {hours_per_day}

## Indian Industry Benchmarks
- FAANG / Top Product: Advanced DSA, System Design, 2+ strong projects
- Tier-1 MNC: Intermediate DSA, one solid project
- Startup Role: Practical skills, 1–2 complete projects, active GitHub
- Higher Studies: Publications or thesis, high GPA, domain expertise

## Output Schema
{{
  "overall_risk_level": "Low | Medium | High | Critical",
  "timeline_risk": {{
    "level": "Low | Medium | High",
    "reason": "string",
    "months_needed": 0,
    "months_available": 0,
    "is_achievable": true
  }},
  "skill_gaps": [
    {{
      "area": "string",
      "severity": "Low | Medium | High | Critical",
      "description": "string",
      "fix_timeline_weeks": 0,
      "priority": 1
    }}
  ],
  "strategic_risks": [
    {{
      "risk": "string",
      "impact": "string",
      "mitigation": "string"
    }}
  ],
  "quick_wins": ["action 1", "action 2"],
  "red_flags": ["flag1"],
  "risk_summary": "2-sentence plain-English summary of the single biggest concern and what to do about it"
}}
"""

class RiskAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.2,
            max_tokens=1000
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT)
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

    async def assess_risk(self, request: RiskAssessmentRequest) -> RiskReportOutput:
        summary_json = json.dumps(request.summary.dict())

        variables = {
            "student_summary_json": summary_json,
            "career_goal": request.profile.career_goal,
            "years_remaining": request.years_remaining,
            "primary_domain": request.profile.primary_domain,
            "hours_per_day": request.hours_per_day
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
            return RiskReportOutput(**parsed_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM output as JSON: {raw_output}") from e
