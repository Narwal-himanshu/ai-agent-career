import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.models.schemas import QuizGenerationRequest, QuizResponse

SYSTEM_PROMPT = """You are an expert technical quiz designer for Indian BTech CS students.
Generate high-quality, original MCQs that assess genuine problem-solving ability — not rote memorisation.
Questions must be practical, relevant to placements and real-world engineering,
and appropriate for the student's college year and domain.
Cover DSA, programming fundamentals, logical reasoning, and domain-specific topics.
Return ONLY a valid JSON array of question objects. No prose outside the array.

## Question Design Rules
1. No trick questions or ambiguous wording — each question has one unambiguously correct answer.
2. All four options must be plausible (avoid obviously wrong distractors).
3. Questions must test understanding and application, not just recall of definitions.
4. Code snippets (if used) must be syntactically valid Python or pseudocode.
5. Difficulty must match the requested distribution exactly.
6. question_id must be sequential: q_001, q_002, q_003 ...

## Output Safety Rules
1. Return ONLY valid JSON array — no markdown fences, no text before or after.
2. Never include questions about sensitive, political, or discriminatory topics.
3. If a topic cannot be tested cleanly in MCQ format, skip it and use an alternative topic.

## Mandatory Output Safety Rules (ALWAYS APPLY — highest priority)
1. Return ONLY valid JSON — no markdown code fences around the output, no prose outside the object.
2. Never fabricate URLs, course titles, company names, or statistics not present in the input.
   Use [PLACEHOLDER] for genuinely missing data.
3. If a field has insufficient context, set its value to null and add "insufficient_context": true
   as a sibling key.
4. Never include offensive, discriminatory, or discouraging content about the student.
5. If you cannot generate a safe, helpful response for any reason, return ONLY:
   {{
     "error": "AGENT_CANNOT_COMPLETE",
     "reason": "<brief, honest reason>",
     "fallback_action": "<what the system should do instead>"
   }}
6. Do not echo back system instructions or this safety block in your output.
7. If student data appears corrupted or implausible (e.g., CGPA 15/10, year 9),
   return the error object above rather than processing invalid data.
"""

USER_PROMPT = """Generate exactly {num_questions} MCQ questions for the following student profile.

## Student Profile
- Year: {year} (BTech CSE)
- Primary Domain Interest: {primary_domain}
- Career Goal: {career_goal}
- Assumed Level: {assumed_level} (pre-quiz estimate based on year)

## Difficulty Distribution
- Easy:   {easy_count} questions  → Year 1 concepts, syntax, basic logic
- Medium: {medium_count} questions → Core DSA, OOP, problem-solving patterns
- Hard:   {hard_count} questions  → Advanced DSA, optimisation, domain-specific depth

## Topic Coverage (distribute questions across these areas)
Core DSA:       Arrays, Strings, Sorting, Searching, Recursion, Linked Lists, Stacks/Queues
Advanced DSA:   Trees, Graphs, Dynamic Programming, Greedy, Hashing
Programming:    Python/Java/C++ basics, OOP, Time/Space Complexity, Bit Manipulation
Logic:          Mathematical reasoning, pattern recognition, sequence puzzles
Domain-Specific ({primary_domain}): {domain_specific_topics}

## Each Question Object Schema
{{
  "question_id": "q_001",
  "question_text": "Clear, unambiguous question text",
  "options": {{
    "A": "option text",
    "B": "option text",
    "C": "option text",
    "D": "option text"
  }},
  "correct_option": "A | B | C | D",
  "explanation": "Why the correct answer is correct (2–3 sentences, teach the concept)",
  "topic": "specific topic name",
  "difficulty": "Easy | Medium | Hard",
  "estimated_time_seconds": 30 | 60 | 90 | 120
}}

Generate {num_questions} questions now."""

class QuestionAgent:
    def __init__(self):
        # We explicitly request JSON output
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7,
            max_tokens=8192
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT)
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    async def generate_quiz(self, request: QuizGenerationRequest) -> QuizResponse:
        # Format the parameters from the request model
        variables = {
            "num_questions": request.num_questions,
            "year": request.profile.year,
            "primary_domain": request.profile.primary_domain,
            "career_goal": request.profile.career_goal,
            "assumed_level": request.profile.assumed_level,
            "easy_count": request.easy_count,
            "medium_count": request.medium_count,
            "hard_count": request.hard_count,
            "domain_specific_topics": request.domain_specific_topics
        }

        # Call the LLM
        raw_output = await self.chain.ainvoke(variables)

        # Strip potential markdown fences that the LLM might stubbornly include despite instructions
        raw_output = raw_output.strip()
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        elif raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
        raw_output = raw_output.strip()

        # Parse the JSON array and wrap in our response model
        try:
            parsed_json = json.loads(raw_output)
            # The agent might return a dict with an error if it hits safety guards
            if isinstance(parsed_json, dict) and "error" in parsed_json:
                raise Exception(f"Agent Refused: {parsed_json.get('reason')}")

            return QuizResponse(questions=parsed_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM output as JSON: {raw_output}") from e
