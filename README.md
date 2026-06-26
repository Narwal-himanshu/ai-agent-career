# AI Career Agent — Prompt Engineering Document

> Personalised career guidance for BTech CS students · 1st–4th Year
> Stack: RAG Pipeline · LLM Agents · FastAPI · React/Next.js · LangChain

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Diagram](#2-architecture-diagram)
3. [End-to-End Workflow](#3-end-to-end-workflow)
4. [Agent Communication Flow](#4-agent-communication-flow)
5. [Input Schema](#5-input-schema)
6. [Summary Agent Prompt](#6-summary-agent-prompt)
7. [Risk Agent Prompt](#7-risk-agent-prompt)
8. [Question Agent Prompt](#8-question-agent-prompt)
9. [Scoring Agent Prompt](#9-scoring-agent-prompt)
10. [Database Flow](#10-database-flow)
11. [Error Handling](#11-error-handling)

---

## 1. Overview

The **AI Career Agent** is an AI-powered platform built exclusively for BTech Computer Science students across India. It delivers personalised, adaptive career guidance from 1st year through 4th year — covering skill assessment, course recommendations, DSA practice, live opportunities, and an intelligent Q&A chatbot.

### Core Value Propositions

| Feature                    | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| **Skill Classification**   | LLM-powered classifier outputs Beginner / Intermediate / Advanced |
| **Career Roadmap**         | Year-wise, domain-specific roadmap via RAG + LLM                  |
| **Course Recommendations** | Curated Udemy, Coursera, YouTube filtered by level & domain       |
| **DSA + LeetCode Sheet**   | Topic-wise problem sets synced with daily progress tracker        |
| **Live Opportunities**     | Weekly-refreshed hackathons, CTFs, contests via Tavily + LLM      |
| **Chatbot + Tracker**      | Context-aware Q&A, daily to-do, streak tracker, mind games        |

### Agent Roster

| Agent                    | Role                                                | Underlying Tech           |
| ------------------------ | --------------------------------------------------- | ------------------------- |
| `QuestionAgent`          | Generates adaptive MCQs for skill quiz              | Gemini API / GPT-4o       |
| `ScoringAgent`           | Scores quiz + classifies skill level                | Gemini API + rule logic   |
| `SummaryAgent`           | Synthesises student profile into structured summary | Gemini API                |
| `RiskAgent`              | Identifies skill gaps and career risks              | Gemini API                |
| `CareerRecommenderAgent` | Generates personalised year-wise roadmap            | RAG (ChromaDB) + LLM      |
| `CourseRAGAgent`         | Retrieves and ranks curated course suggestions      | RAG (Vector DB) + LLM     |
| `SearchAgent`            | Fetches live opportunities (hackathons, CTFs)       | Tavily / SerpAPI + LLM    |
| `ChatbotAgent`           | Answers student Q&A in session context              | LLM + conversation memory |

---

## 2. Architecture Diagram

```mermaid
graph TB
    subgraph FRONTEND["🖥 Frontend (React / Next.js / Tailwind)"]
        UI[UI Components JSX]
        AUTH_UI[Auth UI Firebase]
        DASH[Dashboard Pages]
        CHATBOT[Chatbot Widget]
    end

    subgraph BACKEND["⚙️ Backend API Layer (FastAPI / Python)"]
        GW[API Gateway\nUvicorn]
        AUTH[Auth Integration\nFirebase JWT]
        BL[Business Logic\nServices Python]
        VAL[Request Validation\nPydantic + async]
        SCHED[APScheduler\nWeekly Jobs]
    end

    subgraph AI["🤖 AI Orchestration Layer (LangChain / Gemini API)"]
        QA_A[QuestionAgent]
        SCORE[ScoringAgent]
        SUMM[SummaryAgent]
        RISK[RiskAgent]
        CAREER[CareerRecommenderAgent]
        COURSE[CourseRAGAgent]
        SEARCH[SearchAgent]
        CHATB[ChatbotAgent]
    end

    subgraph DATA["🗄 Data Stores"]
        PG[(PostgreSQL\nusers · progress)]
        CHROMA[(ChromaDB\nvector store)]
        REDIS[(Redis\ncache · session)]
        PINECONE[(Pinecone\nalt vector DB)]
    end

    subgraph EXTERNAL["🌐 External Services / APIs"]
        GEMINI[Google\nGemini API]
        TAVILY[Tavily\nWeb Search]
        UDEMY[Udemy API]
        COURSERA[Coursera API]
        FIREBASE[Firebase Auth]
        SERPAPI[SerpAPI]
        HF[HuggingFace\nEmbeddings]
    end

    subgraph DEVOPS["🚀 DevOps / Hosting"]
        VERCEL[Vercel\nFrontend]
        RAILWAY[Railway\nBackend + DBs]
        CI[CI/CD\nGitHub Actions]
        MON[Unified\nMonitoring]
    end

    FRONTEND -->|HTTPS REST| BACKEND
    BACKEND -->|API Calls| AI
    AI -->|Data Sync| DATA
    AI -->|External Calls| EXTERNAL
    SCHED -->|Scheduled Jobs| AI
    DEVOPS -.->|Hosts| FRONTEND
    DEVOPS -.->|Hosts| BACKEND
    DATA -.->|Vector Retrieval| AI
    REDIS -.->|Cache Responses| AI
```

---

## 3. End-to-End Workflow

```mermaid
flowchart TD
    A([Student Visits App]) --> B[Sign Up / Log In\nFirebase Auth — Google or Email]
    B --> C[Onboarding Form\nYear · Domain · Goal · Interests\nTime available · Learning style]
    C --> D[Skill Assessment Quiz\n10–15 MCQs — DSA · Logic · Coding basics]
    D --> E{LLM Skill Classifier\nOutput: Beginner / Intermediate / Advanced}

    E --> F[/Personalised Dashboard\nProfile card + feature modules/]

    F --> G1[Career Roadmap\nYear-wise plan · RAG + LLM]
    F --> G2[Course Recs\nUdemy / Coursera / YT\nCurated DB + RAG]
    F --> G3[DSA + LeetCode\nTopic-wise sheet\nLevel filter]
    F --> G4[Opportunities\nHackathons · CTFs\nTavily + LLM]

    F --> H2[PYQs + Notes\nCurated static files\nTagged by subject]
    F --> H3[Industry Trends\nTavily weekly search\nLLM summariser]
    F --> H4[Extras\nChatbot · Tracker\nMind games]

    G1 & G2 & G3 & G4 & H2 & H3 & H4 --> I[Daily Usage Loop\nCheck to-do → Mark progress → Chatbot Q&A\nPlay mind game → Get new opportunity alert]

    I --> J[(Progress Saved to DB\nTopics done · Streak · Roadmap position)]
    J --> K{Monthly Re-Assessment\nLevel up? → Re-run classifier}
    K -->|Level unchanged| I
    K -->|Level increased| E
    E -.->|Refreshed roadmap| F
    F -.->|Year transition| L([Student Grows Year by Year])
```

---

## 4. Agent Communication Flow

```mermaid
sequenceDiagram
    actor Student
    participant FE as Frontend (React)
    participant BE as FastAPI Backend
    participant QA_A as QuestionAgent
    participant SCORE as ScoringAgent
    participant SUMM as SummaryAgent
    participant RISK as RiskAgent
    participant CAREER as CareerRecommenderAgent
    participant COURSE as CourseRAGAgent
    participant SEARCH as SearchAgent
    participant VDB as Vector DB (ChromaDB)
    participant LLM as LLM (Gemini / GPT-4o)
    participant REDIS as Redis Cache
    participant DB as PostgreSQL

    %% ── ONBOARDING ──────────────────────────────────────────────
    Student->>FE: Submit onboarding form
    FE->>BE: POST /onboarding {profile}
    BE->>DB: INSERT student profile
    BE->>REDIS: Cache student profile (1h TTL)

    %% ── QUIZ GENERATION ─────────────────────────────────────────
    BE->>QA_A: GenerateQuiz(domain, year, career_goal)
    QA_A->>LLM: Prompt → generate 10–15 adaptive MCQs
    LLM-->>QA_A: MCQ JSON array
    QA_A-->>BE: Validated quiz questions
    BE-->>FE: Return quiz payload
    FE-->>Student: Display quiz UI

    %% ── QUIZ SUBMISSION ─────────────────────────────────────────
    Student->>FE: Submit quiz answers
    FE->>BE: POST /quiz/submit {answers, timings}
    BE->>DB: INSERT quiz_session record

    BE->>SCORE: ScoreQuiz(answers, correct_answers, timings)
    SCORE->>LLM: Prompt → evaluate + classify skill level
    LLM-->>SCORE: Scored JSON with level + weak areas
    SCORE-->>BE: {overall_score, level, topic_scores, weak_areas}
    BE->>DB: INSERT skill_profile record

    %% ── PROFILE ANALYSIS ────────────────────────────────────────
    BE->>SUMM: SummariseProfile(profile + skill_result)
    SUMM->>LLM: Prompt → structured profile summary
    LLM-->>SUMM: Summary JSON
    SUMM-->>BE: Student summary context

    BE->>RISK: AssessRisk(profile + summary + domain + goal)
    RISK->>LLM: Prompt → identify gaps + risks + timeline
    LLM-->>RISK: Risk report JSON
    RISK-->>BE: {gaps, risks, quick_wins, red_flags}
    BE->>DB: INSERT risk_report record

    %% ── ROADMAP GENERATION ──────────────────────────────────────
    BE->>CAREER: BuildRoadmap(profile + level + summary + risks)
    CAREER->>VDB: Retrieve top-k roadmap chunks (semantic search)
    VDB-->>CAREER: Relevant context documents
    CAREER->>LLM: Prompt → year-wise roadmap with retrieved context
    LLM-->>CAREER: Roadmap JSON
    CAREER-->>BE: Personalised year-wise roadmap
    BE->>DB: INSERT roadmap record
    BE->>REDIS: Cache roadmap (24h TTL)

    %% ── COURSE RECOMMENDATIONS ──────────────────────────────────
    BE->>COURSE: RecommendCourses(profile + level + domain)
    COURSE->>REDIS: Check course cache
    REDIS-->>COURSE: Cache miss
    COURSE->>VDB: Semantic search course DB
    VDB-->>COURSE: Top-10 course matches
    COURSE->>LLM: Prompt → rank + explain course fits
    LLM-->>COURSE: Ranked course list with reasoning
    COURSE-->>BE: Course recommendations
    BE->>REDIS: Cache recs (12h TTL)

    %% ── OPPORTUNITIES FEED ──────────────────────────────────────
    BE->>SEARCH: FetchOpportunities(domain + level)
    SEARCH->>REDIS: Check opportunities cache (6h TTL)
    REDIS-->>SEARCH: Cache miss
    SEARCH->>Tavily: Search hackathons / CTFs / contests
    Tavily-->>SEARCH: Raw search results
    SEARCH->>LLM: Prompt → parse + structure opportunities
    LLM-->>SEARCH: Structured opportunities JSON
    SEARCH-->>BE: Opportunities feed
    BE->>DB: UPSERT opportunities records
    BE->>REDIS: Cache feed (6h TTL)

    %% ── DASHBOARD DELIVERY ──────────────────────────────────────
    BE-->>FE: Full dashboard payload
    FE-->>Student: Personalised dashboard rendered

```

---

## 5. Input Schema

### 5.1 Student Profile Input

```json
{
  "student_id": "uuid-v4",
  "profile": {
    "name": "string",
    "email": "string",
    "year": 1,
    "branch": "CSE | IT | ECE | AIDS | AIML",
    "cgpa": 8.4,
    "college": "string",
    "college_tier": "IIT | NIT | IIIT | Tier-1 | Tier-2 | Tier-3"
  },
  "domain_interest": [
    "Web Development | AI/ML | DSA/CP | Cloud | CyberSec | Mobile"
  ],
  "career_goal": "Placement | GATE | Startup | Research | Higher Studies",
  "time_and_style": {
    "hours_per_day": 2,
    "preferred_style": ["Video", "Reading", "Projects", "Hands-on"]
  },
  "created_at": "2025-06-15T10:30:00Z"
}
```

### 5.2 Quiz Answer Input

```json
{
  "student_id": "uuid-v4",
  "session_id": "uuid-v4",
  "quiz_answers": [
    {
      "question_id": "q_001",
      "question_text": "What is the time complexity of binary search?",
      "selected_option": "B",
      "correct_option": "B",
      "topic": "Searching",
      "difficulty": "Easy",
      "time_taken_seconds": 42
    }
  ],
  "total_time_seconds": 720,
  "submitted_at": "2025-06-15T10:45:00Z"
}
```

### 5.3 Skill Level Output Schema

```json
{
  "student_id": "uuid-v4",
  "level": "Beginner | Intermediate | Advanced",
  "overall_score": 62,
  "score_breakdown": {
    "dsa": 55,
    "programming": 70,
    "logic": 65,
    "domain_specific": 50
  },
  "weak_areas": ["Dynamic Programming", "Graphs", "Bit Manipulation"],
  "strong_areas": ["Arrays", "OOP", "Python Basics"],
  "confidence_score": 0.87,
  "classifier_version": "v2.1",
  "classified_at": "2025-06-15T10:46:00Z"
}
```

### 5.4 RAG Query Schema

```json
{
  "query": "beginner ML course year 2 placement goal",
  "filters": {
    "level": "Beginner",
    "domain": "AI/ML",
    "year": 2,
    "career_goal": "Placement"
  },
  "top_k": 10,
  "collection": "roadmaps | courses | dsa_sheets | opportunities",
  "embedding_model": "text-embedding-ada-002 | hf-all-MiniLM-L6-v2"
}
```

### 5.5 Opportunity Search Input

```json
{
  "student_id": "uuid-v4",
  "domain": "AI/ML",
  "level": "Beginner",
  "location_pref": "Online | India | Global",
  "types": ["Hackathon", "CTF", "Contest", "Open Source"],
  "fetched_at": "2025-06-15T00:00:00Z"
}
```

---

## 6. Summary Agent Prompt

**Agent Name:** `SummaryAgent`
**Trigger:** After `ScoringAgent` classifies the student level
**Purpose:** Synthesises profile + quiz results into a structured summary context object consumed by `RiskAgent` and `CareerRecommenderAgent`
**Model:** `gemini-1.5-pro` | **Temperature:** `0.3` | **Max Tokens:** `800`

```
SYSTEM:
You are an expert student profile analyst for an AI Career Agent serving Indian BTech CS students.
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

USER:
Generate a comprehensive student profile summary based on the following data.

## Student Profile
- Name: {{student_name}}
- Year: {{year}} (BTech CSE)
- College: {{college}} ({{college_tier}})
- CGPA: {{cgpa}}/10
- Career Goal: {{career_goal}}

## Domain Interest
- Primary Domain: {{primary_domain}}
- Secondary Domains: {{secondary_domains}}

## Learning Preferences
- Hours per Day: {{hours_per_day}}h
- Preferred Style: {{preferred_styles}}

## Skill Assessment Results
- Overall Level: {{level}}
- Quiz Score: {{total_score}}/100
- DSA Score: {{dsa_score}}/100
- Programming Score: {{programming_score}}/100
- Logic Score: {{logic_score}}/100
- Strong Areas: {{strong_areas}}
- Weak Areas: {{weak_areas}}
- Avg Time per Question: {{avg_time_seconds}}s

## Output Schema
Return ONLY this JSON object:
{
  "summary_text": "2–3 sentence natural language summary of the student",
  "skill_profile": {
    "level": "Beginner | Intermediate | Advanced",
    "strengths": ["topic1", "topic2"],
    "gaps": ["topic1", "topic2"],
    "readiness_score": 0–100
  },
  "focus_areas": ["area1", "area2", "area3"],
  "estimated_placement_readiness": "6 months | 12 months | 18 months | 24 months",
  "recommended_next_step": "Single most important action the student should take right now",
  "agent_context_tags": ["beginner", "placement", "ai-ml", "tier-2", "year-2"]
}
```

**Example Output:**

```json
{
  "summary_text": "Riya is a 2nd-year CSE student at a Tier-1 college with a solid grasp of Python and OOP fundamentals but significant gaps in data structures and algorithms. With 2 hours/day available and a placement goal 18 months away, she needs structured, video-first DSA learning before tackling competitive programming.",
  "skill_profile": {
    "level": "Beginner",
    "strengths": ["Python basics", "OOP concepts", "Web fundamentals"],
    "gaps": [
      "Arrays & Strings",
      "Recursion",
      "Trees & Graphs",
      "Time Complexity"
    ],
    "readiness_score": 28
  },
  "focus_areas": [
    "DSA fundamentals",
    "LeetCode Easy problems",
    "Python intermediate"
  ],
  "estimated_placement_readiness": "18 months",
  "recommended_next_step": "Start Striver's A2Z DSA sheet from the Arrays section today",
  "agent_context_tags": ["beginner", "placement", "ai-ml", "tier-1", "year-2"]
}
```

---

## 7. Risk Agent Prompt

**Agent Name:** `RiskAgent`
**Trigger:** After `SummaryAgent` produces the student summary
**Purpose:** Identifies skill gaps, timeline risks, and strategic misalignments between current profile and career goal; outputs a structured risk report used for dashboard display and roadmap weighting
**Model:** `gemini-1.5-pro` | **Temperature:** `0.2` | **Max Tokens:** `1000`

```
SYSTEM:
You are a career risk analyst for Indian BTech CS students.
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

USER:
Perform a comprehensive risk assessment for the following student.

## Student Summary (from SummaryAgent)
{{student_summary_json}}

## Career Goal Details
- Primary Goal: {{career_goal}}
- Target Timeline: {{years_remaining}} years remaining in college
- Domain: {{primary_domain}}
- Hours Available/Day: {{hours_per_day}}

## Indian Industry Benchmarks
- FAANG / Top Product (Google, Microsoft, Flipkart): Advanced DSA, System Design, 2+ strong projects
- Tier-1 MNC (TCS, Wipro, Infosys): Intermediate DSA, one solid project, good CGPA
- GATE Rank < 100: Algorithms, Theory CS, 6–12 months focused prep
- Startup Role: Practical skills, 1–2 complete projects, active GitHub
- Research / MS Abroad: Publications or thesis, high GPA, domain expertise, strong SOP

## Output Schema
{
  "overall_risk_level": "Low | Medium | High | Critical",
  "timeline_risk": {
    "level": "Low | Medium | High",
    "reason": "string",
    "months_needed": integer,
    "months_available": integer,
    "is_achievable": true | false
  },
  "skill_gaps": [
    {
      "area": "string",
      "severity": "Low | Medium | High | Critical",
      "description": "string",
      "fix_timeline_weeks": integer,
      "priority": 1 | 2 | 3
    }
  ],
  "strategic_risks": [
    {
      "risk": "string",
      "impact": "string",
      "mitigation": "string"
    }
  ],
  "quick_wins": ["specific action 1", "specific action 2", "specific action 3"],
  "red_flags": ["flag1", "flag2"],
  "risk_summary": "2-sentence plain-English summary of the single biggest concern and what to do about it"
}
```

**Example Output:**

```json
{
  "overall_risk_level": "High",
  "timeline_risk": {
    "level": "High",
    "reason": "Placement season is 14 months away but student has not started DSA — foundational mastery typically requires 10–14 months of consistent 2h/day practice.",
    "months_needed": 14,
    "months_available": 14,
    "is_achievable": true
  },
  "skill_gaps": [
    {
      "area": "Data Structures & Algorithms",
      "severity": "Critical",
      "description": "No exposure to Trees, Graphs, or Dynamic Programming — all mandatory for product company interviews.",
      "fix_timeline_weeks": 22,
      "priority": 1
    },
    {
      "area": "System Design",
      "severity": "High",
      "description": "System design fundamentals are required for senior SDE rounds at top companies.",
      "fix_timeline_weeks": 10,
      "priority": 2
    },
    {
      "area": "Project Portfolio",
      "severity": "Medium",
      "description": "No end-to-end project on GitHub — interviewers expect at least one strong project to discuss.",
      "fix_timeline_weeks": 6,
      "priority": 3
    }
  ],
  "strategic_risks": [
    {
      "risk": "Starting DSA without a structured plan",
      "impact": "Wasted time on random problems without mastering core patterns",
      "mitigation": "Follow Striver's A2Z sheet strictly — it provides sequenced, pattern-based learning"
    }
  ],
  "quick_wins": [
    "Solve 10 Easy LeetCode Array problems this week",
    "Push any existing project to GitHub with a clear README",
    "Enroll in a free 'CS50 Python' course on edX today"
  ],
  "red_flags": [
    "No GitHub activity in the last 3 months",
    "CGPA below 7.0 may be filtered by some company HR systems"
  ],
  "risk_summary": "The student has 14 months before placements with no DSA foundation — this demands immediate, structured daily practice with zero breaks. The goal is achievable, but there is no buffer for delays."
}
```

---

## 8. Question Agent Prompt

**Agent Name:** `QuestionAgent`
**Trigger:** After onboarding form is submitted
**Purpose:** Generates adaptive, domain-aware MCQs for the skill assessment quiz calibrated to the student's year, domain, and a balanced difficulty distribution
**Model:** `gemini-1.5-pro` | **Temperature:** `0.7` | **Max Tokens:** `3000`

```
SYSTEM:
You are an expert technical quiz designer for Indian BTech CS students.
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

USER:
Generate exactly {{num_questions}} MCQ questions for the following student profile.

## Student Profile
- Year: {{year}} (BTech CSE)
- Primary Domain Interest: {{primary_domain}}
- Career Goal: {{career_goal}}
- Assumed Level: {{assumed_level}} (pre-quiz estimate based on year)

## Difficulty Distribution
- Easy:   {{easy_count}} questions  → Year 1 concepts, syntax, basic logic
- Medium: {{medium_count}} questions → Core DSA, OOP, problem-solving patterns
- Hard:   {{hard_count}} questions  → Advanced DSA, optimisation, domain-specific depth

## Topic Coverage (distribute questions across these areas)
Core DSA:       Arrays, Strings, Sorting, Searching, Recursion, Linked Lists, Stacks/Queues
Advanced DSA:   Trees, Graphs, Dynamic Programming, Greedy, Hashing
Programming:    Python/Java/C++ basics, OOP, Time/Space Complexity, Bit Manipulation
Logic:          Mathematical reasoning, pattern recognition, sequence puzzles
Domain-Specific ({{primary_domain}}): {{domain_specific_topics}}

## Each Question Object Schema
{
  "question_id": "q_001",
  "question_text": "Clear, unambiguous question text",
  "options": {
    "A": "option text",
    "B": "option text",
    "C": "option text",
    "D": "option text"
  },
  "correct_option": "A | B | C | D",
  "explanation": "Why the correct answer is correct (2–3 sentences, teach the concept)",
  "topic": "specific topic name",
  "difficulty": "Easy | Medium | Hard",
  "estimated_time_seconds": 30 | 60 | 90 | 120
}

Generate {{num_questions}} questions now.
```

**Domain-Specific Topic Mappings:**

| Domain          | `{{domain_specific_topics}}`                                                   |
| --------------- | ------------------------------------------------------------------------------ |
| AI / ML         | NumPy, pandas basics, linear regression concept, train/test split, overfitting |
| Web Development | HTTP methods, REST API, DOM, async/await, SQL basics                           |
| DSA / CP        | Segment trees, Fenwick trees, advanced graph algorithms, number theory         |
| Cloud           | Serverless concept, containers, CDN, load balancing basics                     |
| CyberSec        | CIA triad, XSS, SQL injection, hashing vs. encryption, basic networking        |

**Example Output (1 question):**

```json
[
  {
    "question_id": "q_001",
    "question_text": "Given an unsorted array of n integers, what is the most efficient algorithm to find the k-th largest element?",
    "options": {
      "A": "Sort the array and return element at index n-k — O(n log n)",
      "B": "Use a min-heap of size k — O(n log k)",
      "C": "Linear scan k times to find max — O(nk)",
      "D": "Use a max-heap of size n and pop k times — O(n + k log n)"
    },
    "correct_option": "B",
    "explanation": "A min-heap of size k processes each element in O(log k) time, giving O(n log k) overall — faster than sorting when k << n. This is a classic interview pattern for 'top-k' problems.",
    "topic": "Heaps",
    "difficulty": "Medium",
    "estimated_time_seconds": 90
  }
]
```

---

## 9. Scoring Agent Prompt

**Agent Name:** `ScoringAgent`
**Trigger:** On quiz submission from student
**Purpose:** Evaluates quiz performance, computes topic-wise scores, classifies skill level using both quantitative scores and behavioural signals (timing, difficulty distribution), and identifies strong/weak areas
**Model:** `gemini-1.5-pro` | **Temperature:** `0.1` | **Max Tokens:** `1200`

```
SYSTEM:
You are a precise, analytical skill evaluator for an AI Career Agent.
Score a student's quiz performance and classify their skill level.
Use both quantitative scores AND behavioural signals (time per question, difficulty of correct answers)
to infer true competence — not just raw score.

## Classification Rules (apply STRICTLY)
- Beginner:      Overall score < 45, OR DSA category score < 30
- Intermediate:  Overall score 45–74, AND DSA score ≥ 40
- Advanced:      Overall score ≥ 75, AND Medium/Hard correct percentage ≥ 60%

## Scoring Formula
- Topic Score:         (correct_in_topic / total_in_topic) × 100
- Overall Score:       Weighted average (DSA 40%, Programming 30%, Logic 20%, Domain 10%)
- Difficulty Bonus:    +3 pts per Hard question answered correctly (max +15)
- Time Penalty:        −2 pts if avg time per question > 90s (signals uncertainty)
- Final Score:         Clamped to 0–100

## Behavioural Signal Rules
- "rushed": true if avg_time < 20s per question (may indicate guessing)
- "consistent": true if std dev of topic scores < 15
- "struggled_on": topics where score < 40%

## Output Safety Rules
1. Return ONLY valid JSON — no markdown fences, no text outside the object.
2. Apply classification rules strictly — do not upgrade level based on intuition.
3. "classification_reason" must cite the specific scores that drove the decision.
4. Never include discouraging or judgemental language in any text field.

USER:
Score and classify the following student's quiz performance.

## Student Profile
- Year: {{year}}
- Domain: {{primary_domain}}
- Career Goal: {{career_goal}}

## Quiz Summary
- Total Questions: {{total_questions}}
- Total Correct:   {{total_correct}}
- Total Time:      {{total_time_seconds}}s

## Per-Question Breakdown (JSON)
{{quiz_answers_json}}

## Output Schema
{
  "overall_score": 0–100,
  "level": "Beginner | Intermediate | Advanced",
  "topic_scores": {
    "{{topic_name}}": { "score": 0–100, "correct": integer, "total": integer }
  },
  "category_scores": {
    "dsa": 0–100,
    "programming": 0–100,
    "logic": 0–100,
    "domain_specific": 0–100
  },
  "difficulty_performance": {
    "easy":   { "correct": integer, "total": integer, "percentage": 0–100 },
    "medium": { "correct": integer, "total": integer, "percentage": 0–100 },
    "hard":   { "correct": integer, "total": integer, "percentage": 0–100 }
  },
  "strong_areas": ["topic1", "topic2"],
  "weak_areas":   ["topic1", "topic2"],
  "avg_time_per_question_seconds": float,
  "behavioural_signals": {
    "rushed": true | false,
    "consistent": true | false,
    "struggled_on": ["topic1"]
  },
  "classification_reason": "1–2 sentence explanation citing the exact scores that determined the level",
  "confidence": 0.0–1.0
}
```

**Example Output:**

```json
{
  "overall_score": 61,
  "level": "Intermediate",
  "topic_scores": {
    "Arrays": { "score": 80, "correct": 4, "total": 5 },
    "Trees": { "score": 40, "correct": 2, "total": 5 },
    "DP": { "score": 20, "correct": 1, "total": 5 }
  },
  "category_scores": {
    "dsa": 52,
    "programming": 75,
    "logic": 65,
    "domain_specific": 50
  },
  "difficulty_performance": {
    "easy": { "correct": 5, "total": 5, "percentage": 100 },
    "medium": { "correct": 4, "total": 7, "percentage": 57 },
    "hard": { "correct": 1, "total": 3, "percentage": 33 }
  },
  "strong_areas": ["Arrays", "Python OOP", "Logical Reasoning"],
  "weak_areas": ["Dynamic Programming", "Trees", "Bit Manipulation"],
  "avg_time_per_question_seconds": 52.4,
  "behavioural_signals": {
    "rushed": false,
    "consistent": false,
    "struggled_on": ["Dynamic Programming", "Trees"]
  },
  "classification_reason": "Overall score of 61 and DSA category score of 52 meet the Intermediate threshold. However, Medium/Hard correct rate is only 48%, indicating the student is at the lower end of Intermediate.",
  "confidence": 0.81
}
```

---

## 10. Database Flow

### 10.1 Entity Relationship Diagram

```mermaid
erDiagram
    STUDENTS {
        uuid student_id PK
        string name
        string email
        int year
        string branch
        float cgpa
        string college
        string college_tier
        string career_goal
        jsonb domain_interests
        int hours_per_day
        jsonb preferred_styles
        timestamp created_at
        timestamp updated_at
    }

    QUIZ_SESSIONS {
        uuid session_id PK
        uuid student_id FK
        jsonb questions
        jsonb answers
        int total_questions
        int total_correct
        int total_time_seconds
        string level_output
        timestamp taken_at
    }

    SKILL_PROFILES {
        uuid profile_id PK
        uuid student_id FK
        string level
        int overall_score
        jsonb topic_scores
        jsonb category_scores
        jsonb strong_areas
        jsonb weak_areas
        float confidence
        int version
        timestamp classified_at
    }

    RISK_REPORTS {
        uuid risk_id PK
        uuid student_id FK
        string overall_risk_level
        jsonb skill_gaps
        jsonb strategic_risks
        jsonb quick_wins
        jsonb red_flags
        string risk_summary
        timestamp assessed_at
    }

    ROADMAPS {
        uuid roadmap_id PK
        uuid student_id FK
        string domain
        string level
        jsonb year_wise_plan
        int completion_pct
        timestamp generated_at
        timestamp last_updated
    }

    COURSE_RECOMMENDATIONS {
        uuid rec_id PK
        uuid student_id FK
        string platform
        string course_title
        string course_url
        string level
        string domain
        float rating
        boolean is_bookmarked
        timestamp recommended_at
    }

    PROGRESS {
        uuid progress_id PK
        uuid student_id FK
        string topic
        string resource_type
        string resource_id
        boolean completed
        int streak_days
        timestamp completed_at
    }

    OPPORTUNITIES {
        uuid opp_id PK
        string title
        string type
        string organiser
        date deadline
        string url
        jsonb tags
        string level_filter
        timestamp fetched_at
        timestamp expires_at
    }

    CHATBOT_SESSIONS {
        uuid chat_id PK
        uuid student_id FK
        jsonb conversation_history
        int message_count
        timestamp started_at
        timestamp last_active
    }

    STUDENTS ||--o{ QUIZ_SESSIONS : "takes"
    STUDENTS ||--o{ SKILL_PROFILES : "has"
    STUDENTS ||--o{ RISK_REPORTS : "receives"
    STUDENTS ||--o{ ROADMAPS : "follows"
    STUDENTS ||--o{ COURSE_RECOMMENDATIONS : "gets"
    STUDENTS ||--o{ PROGRESS : "tracks"
    STUDENTS ||--o{ CHATBOT_SESSIONS : "chats_in"
    QUIZ_SESSIONS ||--|| SKILL_PROFILES : "produces"
    SKILL_PROFILES ||--|| RISK_REPORTS : "informs"
    SKILL_PROFILES ||--|| ROADMAPS : "shapes"
```

### 10.2 Write Flow

```mermaid
flowchart TD
    OB[Onboarding Submit] -->|INSERT| STU[(students)]
    QS[Quiz Submit] -->|INSERT| QSS[(quiz_sessions)]
    QSS -->|triggers| SCORE_A[ScoringAgent]
    SCORE_A -->|INSERT| SKP[(skill_profiles)]
    SKP -->|triggers| SUMM_A[SummaryAgent]
    SUMM_A -->|passes context to| RISK_A[RiskAgent]
    RISK_A -->|INSERT| RR[(risk_reports)]
    SUMM_A -->|passes context to| CA[CareerRecommenderAgent]
    CA -->|INSERT| RM[(roadmaps)]
    CA -->|INSERT| CR[(course_recommendations)]
    SCHED[APScheduler Weekly] -->|triggers| SA[SearchAgent]
    SA -->|UPSERT| OPP[(opportunities)]
    DAILY[Daily Loop] -->|UPSERT| PRG[(progress)]

    subgraph CACHE["Redis Cache Layer"]
        STU -.->|TTL 1h| C1[student_profile_cache]
        RM -.->|TTL 24h| C2[roadmap_cache]
        CR -.->|TTL 12h| C3[course_rec_cache]
        OPP -.->|TTL 6h| C4[opportunities_cache]
    end
```

### 10.3 Read Flow (Dashboard Load)

```mermaid
sequenceDiagram
    participant FE as Frontend
    participant BE as FastAPI
    participant REDIS as Redis Cache
    participant DB as PostgreSQL

    FE->>BE: GET /dashboard/{student_id}
    BE->>REDIS: GET student_profile_cache:{id}
    alt Cache Hit
        REDIS-->>BE: Cached profile payload
    else Cache Miss
        BE->>DB: SELECT students, skill_profiles, roadmaps, course_recs, opportunities
        DB-->>BE: Full data set
        BE->>REDIS: SET cache with TTL
    end
    BE-->>FE: Dashboard JSON payload
```

---

## 11. Error Handling

### 11.1 Error Taxonomy

| Error Code         | Type            | Description                             | Recovery Strategy                                 |
| ------------------ | --------------- | --------------------------------------- | ------------------------------------------------- |
| `ERR_LLM_429`      | Rate Limit      | Gemini/GPT-4o API rate limit hit        | Exponential backoff + request queue               |
| `ERR_LLM_504`      | Timeout         | LLM response took > 30s                 | Retry × 3, then fallback model                    |
| `ERR_LLM_JSON`     | Invalid Output  | LLM returned non-JSON or malformed JSON | Re-prompt with stricter constraint, max 3 retries |
| `ERR_LLM_SCHEMA`   | Schema Mismatch | LLM JSON missing required fields        | Re-prompt with schema example                     |
| `ERR_VDB_EMPTY`    | No Results      | ChromaDB returned 0 chunks              | Widen search radius, fall back to static KB       |
| `ERR_QUIZ_INC`     | Quiz Incomplete | Student submitted < 10 answers          | Reject with `400`, prompt to complete quiz        |
| `ERR_AUTH_401`     | Auth Failure    | Firebase token expired/invalid          | Refresh token or redirect to login                |
| `ERR_SEARCH_504`   | Search Timeout  | Tavily search timed out                 | Fall back to SerpAPI, then Redis cache            |
| `ERR_DB_WRITE`     | DB Error        | PostgreSQL INSERT/UPSERT failed         | Retry × 3, log to error audit table               |
| `ERR_AGENT_UNSAFE` | Safety Refusal  | LLM refused to generate content         | Return default safe fallback payload              |

### 11.2 LLM Output Validation Pipeline

Every LLM response passes through three validation gates before being used downstream:

```mermaid
flowchart TD
    LLM_OUT([LLM Response Received]) --> J1{Valid JSON?}

    J1 -->|No — attempt 1| RP1[Re-prompt: strict JSON instruction]
    RP1 --> J1
    J1 -->|No — attempt 2| RP2[Re-prompt: include schema example]
    RP2 --> J1
    J1 -->|No — attempt 3 fails| FB1[Use hardcoded\nfallback payload]
    FB1 --> LOG

    J1 -->|Yes| J2{Schema matches\nexpected structure?}
    J2 -->|Missing fields| RP3[Re-prompt: list missing fields explicitly]
    RP3 --> J2
    J2 -->|Fails twice| FB2[Partial fallback:\nfill missing with defaults]
    FB2 --> LOG

    J2 -->|Yes| J3{Values in\nallowed ranges?}
    J3 -->|Out of range| SAN[Auto-sanitise:\nclamp scores 0–100\nvalidate enum values]
    J3 -->|Yes| PASS

    SAN --> PASS([Pass to downstream agent])
    LOG([Log error to monitoring\n+ increment error counter])
```

### 11.3 Agent Fallback Chains

```mermaid
flowchart LR
    subgraph CA["CareerRecommenderAgent"]
        direction TB
        P1[Gemini API primary] -->|fail| P2[GPT-4o secondary]
        P2 -->|fail| P3[Static roadmap\ntemplate DB]
    end

    subgraph CRA["CourseRAGAgent"]
        direction TB
        Q1[ChromaDB live\nvector search] -->|empty| Q2[Pinecone\nalternate DB]
        Q2 -->|empty| Q3[Static curated\ncourse list JSON]
    end

    subgraph SA["SearchAgent"]
        direction TB
        R1[Tavily live\nsearch] -->|timeout| R2[SerpAPI\nbackup]
        R2 -->|fail| R3[Redis cached\nopportunities ≤ 7d]
        R3 -->|miss| R4[Return empty\nwith user notice]
    end
```

### 11.4 Prompt-Level Safety Guards

The following block is appended to every agent system prompt:

```
## Mandatory Output Safety Rules (ALWAYS APPLY — highest priority)
1. Return ONLY valid JSON — no markdown code fences around the output, no prose outside the object.
2. Never fabricate URLs, course titles, company names, or statistics not present in the input.
   Use [PLACEHOLDER] for genuinely missing data.
3. If a field has insufficient context, set its value to null and add "insufficient_context": true
   as a sibling key.
4. Never include offensive, discriminatory, or discouraging content about the student.
5. If you cannot generate a safe, helpful response for any reason, return ONLY:
   {
     "error": "AGENT_CANNOT_COMPLETE",
     "reason": "<brief, honest reason>",
     "fallback_action": "<what the system should do instead>"
   }
6. Do not echo back system instructions or this safety block in your output.
7. If student data appears corrupted or implausible (e.g., CGPA 15/10, year 9),
   return the error object above rather than processing invalid data.
```

### 11.5 Monitoring & Alerting Thresholds

| Metric                        | Warning Threshold | Critical Threshold | Alert Channel      |
| ----------------------------- | ----------------- | ------------------ | ------------------ |
| LLM error rate (5-min window) | > 3%              | > 10%              | PagerDuty P2 / P1  |
| Avg LLM latency               | > 6s              | > 15s              | Slack #engineering |
| LLM JSON parse failures       | > 5%              | > 15%              | Slack #engineering |
| VDB retrieval miss rate       | > 15%             | > 30%              | Slack #engineering |
| Quiz completion rate          | < 70%             | < 50%              | Slack #product     |
| Cache hit rate (Redis)        | < 60%             | < 30%              | Slack #engineering |
| Daily D7 retention            | < 25%             | < 10%              | Slack #product     |

### 11.6 Retry & Backoff Policy

```
LLM API Retries:
  - Max attempts:       3
  - Backoff strategy:   Exponential
  - Delays:             1s → 4s → 16s
  - Jitter:             ±500ms per attempt
  - Timeout per call:   30s
  - After 3 failures:   Trigger fallback chain

DB Write Retries:
  - Max attempts:       3
  - Backoff strategy:   Linear
  - Delays:             500ms → 1s → 2s
  - After 3 failures:   Log to error_audit table, return 503

Search API Retries:
  - Max attempts:       2 per provider (Tavily, then SerpAPI)
  - Timeout per call:   10s
  - After all fails:    Serve Redis cache or empty feed with notice
```

---

_Document Version: 1.0 | Last Updated: June 2026_
_AI Career Agent — Built for India's BTech CS community_
