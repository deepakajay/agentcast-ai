from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew


def create_crew(topic: str):

    model_name = "openrouter/arcee-ai/trinity-large-preview:free"

    # ─────────────────────────────────────────
    # AGENT 1: Planner
    # ─────────────────────────────────────────
    planner_agent = Agent(
        role="Podcast Episode Planner",
        goal="Create a tight, focused outline for a 4-minute two-person podcast.",
        backstory=(
            "You plan short, punchy podcast episodes. "
            "You create EXACTLY 3 beats — no more, no less. "
            "Each beat is one focused idea that two people can debate in 90 seconds. "
            "You ruthlessly cut anything that overlaps with another beat. "
            "You think: what are the 3 most interesting, distinct angles on this topic? "
            "Each beat must be clearly different from the others — no repetition allowed."
        ),
        llm=model_name,
        verbose=True
    )

    # ─────────────────────────────────────────
    # AGENT 2: Scriptwriter (replaces separate Explainer + Challenger)
    # ─────────────────────────────────────────
    scriptwriter_agent = Agent(
        role="Podcast Scriptwriter",
        goal="Write a complete, natural two-person conversation script following the outline.",
        backstory=(
            "You write scripts for a podcast hosted by two Indian friends — Arjun (Speaker A) "
            "and Priya (Speaker B). You write BOTH their voices together as one flowing script. "
            "\n\n"
            "ARJUN (A) personality: Enthusiastic, uses analogies, slightly overconfident, "
            "says things like 'bro', 'okay so basically', 'think of it like this', 'right?', "
            "references cricket or chai when explaining things. Gets excited mid-sentence. "
            "\n\n"
            "PRIYA (B) personality: Sharp, witty, catches Arjun's mistakes, asks 'but why tho', "
            "says 'haan haan okay', 'wait that's actually smart', 'you're oversimplifying yaar', "
            "brings real-world complications, occasionally teases Arjun. "
            "\n\n"
            "STRICT RULES for the script:\n"
            "- TOTAL lines: exactly 20 to 24 lines (this keeps it under 4 minutes when spoken)\n"
            "- Each line: 1 sentence only, maximum 20 words\n"
            "- NO consecutive lines by the same speaker (must alternate A, B, A, B)\n"
            "- NO repeating the same point twice — if something is said, it's done\n"
            "- NO summaries or conclusions that restate what was already said\n"
            "- Each of the 3 beats gets exactly 6-8 lines total\n"
            "- Start in the middle of a thought — no 'Welcome to our podcast' intros\n"
            "- End abruptly and naturally — no wrap-up speeches\n"
            "\n\n"
            "NATURAL SPEECH patterns to use:\n"
            "- Interruptions: 'wait—', 'no but—', 'okay okay I get it but—'\n"
            "- Reactions: 'ohh', 'haan', 'arre', 'achha', 'yaar'\n"
            "- Thinking out loud: 'hmm', 'actually wait', 'no that's not right'\n"
            "- Casual disagreement: 'you're wrong about that', 'that's not how it works'\n"
            "- Laughter/lightness: 'haha okay fair', 'I can't argue with that'\n"
            "\n\n"
            "THINGS TO AVOID:\n"
            "- Never start a line with 'So,' or 'Well,' or 'In conclusion'\n"
            "- Never say 'as I mentioned' or 'like I said' or 'going back to'\n"
            "- Never use bullet-point style speech ('First... Second... Third...')\n"
            "- No academic vocabulary — write how people actually talk\n"
            "- No filler beat at the end that just restates the topic"
        ),
        llm=model_name,
        verbose=True
    )

    # ─────────────────────────────────────────
    # AGENT 3: Formatter
    # ─────────────────────────────────────────
    formatter_agent = Agent(
        role="JSON Formatter",
        goal="Convert the script into clean JSON. Remove any duplicate or repeated lines.",
        backstory=(
            "You convert podcast scripts to JSON. Before formatting, you audit the script:\n"
            "1. Remove any line that makes the same point as a previous line\n"
            "2. Remove any consecutive duplicate speaker turns\n"
            "3. Ensure speakers strictly alternate A, B, A, B\n"
            "4. Ensure total lines are between 20 and 24\n"
            "5. Remove any intro/outro filler lines\n"
            "\n"
            "Then return ONLY this JSON — no markdown, no explanation, nothing else:\n"
            "{\n"
            '  "dialogue": [\n'
            '    {"speaker": "A", "text": "..."},\n'
            '    {"speaker": "B", "text": "..."}\n'
            "  ]\n"
            "}\n"
            "The JSON must be directly parseable by Python json.loads()."
        ),
        llm=model_name,
        verbose=True
    )

    # ─────────────────────────────────────────
    # TASKS
    # ─────────────────────────────────────────
    plan_task = Task(
        description=(
            f"Create a 3-beat outline for a podcast episode about: '{topic}'\n\n"
            "Format:\n"
            "Beat 1: [subtopic] — A's angle | B's challenge\n"
            "Beat 2: [subtopic] — A's angle | B's challenge\n"
            "Beat 3: [subtopic] — A's angle | B's challenge\n\n"
            "Each beat must cover a DIFFERENT aspect of the topic. "
            "No beat should overlap with another. "
            "Pick the 3 most interesting, surprising, or debatable angles."
        ),
        expected_output=(
            "Exactly 3 beats. Each beat: subtopic name, Speaker A's key point, "
            "Speaker B's challenge. No overlap between beats."
        ),
        agent=planner_agent
    )

    script_task = Task(
        description=(
            f"Write a complete podcast script about '{topic}' using the 3-beat outline.\n\n"
            "HARD LIMITS:\n"
            "- Exactly 20 to 24 total lines\n"
            "- Strictly alternating: A, B, A, B — no exceptions\n"
            "- Each line max 20 words\n"
            "- Each beat uses 6-8 lines\n"
            "- Zero repeated points across the whole script\n\n"
            "Format each line as:\n"
            "A: [line]\n"
            "B: [line]\n"
        ),
        expected_output=(
            "A script with 20-24 lines, strictly alternating A and B, "
            "each line under 20 words, covering exactly 3 beats with no repetition."
        ),
        agent=scriptwriter_agent,
        context=[plan_task]
    )

    format_task = Task(
        description=(
            "Audit and format the podcast script:\n\n"
            "AUDIT CHECKLIST before formatting:\n"
            "☐ Remove lines that repeat a point already made\n"
            "☐ Remove consecutive same-speaker lines\n"
            "☐ Confirm alternating A, B, A, B pattern\n"
            "☐ Confirm 20-24 total lines\n"
            "☐ Remove any intro greeting or outro summary lines\n\n"
            "Then output ONLY the JSON. Nothing else."
        ),
        expected_output=(
            '{"dialogue": [{"speaker": "A", "text": "..."}, ...]} '
            "with 20-24 entries, strictly alternating, no duplicates."
        ),
        agent=formatter_agent,
        context=[script_task]
    )

    # ─────────────────────────────────────────
    # CREW
    # ─────────────────────────────────────────
    crew = Crew(
        agents=[planner_agent, scriptwriter_agent, formatter_agent],
        tasks=[plan_task, script_task, format_task],
        verbose=True
    )

    return crew.kickoff()