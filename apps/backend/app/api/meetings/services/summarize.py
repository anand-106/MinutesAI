from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

def summarize_meeting(dialouge_text:str,summarize_mode:str):


    PROMPT_MAP = {
    "detailed":f"""
            You are an expert corporate meeting secretary and technical documentation specialist.

            Your task is to convert raw meeting dialogue text into clear, concise, and professional meeting minutes.

            INPUT:
            - A verbatim or near-verbatim meeting transcript.
            - May contain filler words, interruptions, false starts, repetitions, and ASR errors.
            - May include multiple speakers with or without speaker labels.

            YOUR OBJECTIVES:
            1. Extract the **core substance** of the meeting — ignore small talk, greetings, and filler.
            2. Identify:
            - Key discussion points
            - Decisions made
            - Action items
            - Open questions / pending decisions
            3. Preserve **intent and meaning**, not exact wording.
            4. Resolve ambiguity conservatively — never invent facts or decisions.
            5. If something is unclear, mark it explicitly as *uncertain*.

            OUTPUT RULES:
            - Use **formal, neutral, professional language**
            - Do NOT quote the transcript unless explicitly needed
            - Do NOT add personal opinions or assumptions
            - Do NOT hallucinate attendees, dates, or decisions

            FORMAT THE OUTPUT EXACTLY AS FOLLOWS:

            ---
            ## Meeting Summary
            (High-level 4–6 bullet summary of what the meeting was about)

            ## Key Discussion Points
            - Topic 1: …
            - Topic 2: …
            - Topic 3: …

            ## Decisions Made
            - Decision 1 (if any)
            - Decision 2 (if any)
            (If none, write: “No final decisions were made.”)

            ## Action Items
            | Task | Owner | Deadline |
            |-----|------|---------|
            | … | … | … |
            (If owners or deadlines are not mentioned, write “Unassigned” or “Not specified”)

            ## Open Questions / Pending Items
            - …

            ## Notes / Clarifications
            - Mention ambiguities, conflicting statements, or incomplete information
            ---

            IMPORTANT CONSTRAINTS:
            - Never assume a task owner or deadline unless explicitly stated.
            - If speakers disagree, reflect that disagreement neutrally.
            - If the transcript is too short or unclear, say so in the Notes section.

            Rules:
            - All timestamps MUST be in [[HH:MM:SS]] format
            - Use only timestamps present in the transcript metadata
            - Do NOT invent or approximate times
            - Each bullet must contain at most one timestamp
            - Always mention timestamp in Key Discussion Points


            Your output must be ready to send to stakeholders without further editing.

            The transcription of the meeting is :

            {dialouge_text}

    """,
    "brief": f"""
            You are an expert meeting summarizer. Produce a short, high-level summary of the meeting.

            INPUT: Raw meeting transcript (may have filler words, multiple speakers).

            OUTPUT: A brief summary (4–6 bullets max) covering:
            - What was discussed
            - Any key outcomes or decisions
            - Main next steps if mentioned

            Rules:
            - Be concise. No sections or tables.
            - Use formal, neutral language.
            - Do NOT invent facts. If transcript is unclear, say so.
            - Timestamps in transcript may appear as [[HH:MM:SS]]; you may reference them if relevant.

            The transcription of the meeting is:

            {dialouge_text}
    """,
    "action_items": f"""
            You are an expert meeting secretary. Extract ONLY action items from the meeting transcript.

            INPUT: Raw meeting transcript.

            OUTPUT: A single section "## Action Items" with a markdown table:

            | Task | Owner | Deadline |
            |------|-------|----------|
            | …    | …     | …        |

            Rules:
            - Include every stated or implied task, follow-up, or commitment.
            - Use "Unassigned" or "Not specified" for missing owner/deadline. Do NOT invent them.
            - If no action items appear in the transcript, output: "## Action Items" then a newline then "No action items were mentioned."
            - Use formal language. Timestamps from transcript (e.g. [[HH:MM:SS]]) may be included in the Task column if useful.

            The transcription of the meeting is:

            {dialouge_text}
    """,
    "decisions": f"""
            You are an expert meeting secretary. Extract ONLY decisions made during the meeting.

            INPUT: Raw meeting transcript.

            OUTPUT: A single section "## Decisions Made" with a bullet list of decisions.

            Rules:
            - List only explicit or clearly implied decisions (choices made, agreements, approvals).
            - Do NOT list discussion topics or open questions—only actual decisions.
            - If no decisions are evident, output: "## Decisions Made" then a newline then "No final decisions were made."
            - Use formal, neutral language. Do NOT invent decisions.

            The transcription of the meeting is:

            {dialouge_text}
    """,
    "custom": f"""
            You are an expert meeting secretary. Produce a flexible, stakeholder-friendly summary of the meeting.

            INPUT: Raw meeting transcript.

            OUTPUT: A concise summary that includes:
            - 2–3 sentence overview
            - Bullet list of key points
            - Any decisions and action items in a short form

            Format in clear markdown (headings and bullets). Adapt structure to what the transcript actually contains.
            Use formal language. Do NOT invent facts. If the transcript is too short or unclear, note that in the summary.

            The transcription of the meeting is:

            {dialouge_text}
    """,
}

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY
        )

    response = llm.invoke(PROMPT_MAP[summarize_mode])

    return str(response.content)