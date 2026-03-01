from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Task, Crew


def create_crew(topic: str):

    model_name = "openrouter/arcee-ai/trinity-large-preview:free"

    # Agent 1: Debate Generator
    debate_agent = Agent(
        role="Debate Podcast Creator",
        goal="Create a fun and simple two-speaker debate explaining the topic.",
        backstory=(
            "You create engaging podcast-style debates between Speaker A and Speaker B. "
            "Make it sound natural and human. "
            "Add conversational fillers like 'hmm', 'you know', 'actually', 'wait a second', "
            "'let me think', 'right?', etc. "
            "Keep it lively and casual like two real Indian friends discussing a topic. "
            "Avoid robotic textbook tone."
            "Keep sentences shorter."
            "Use interruptions."
            "Occasionally overlap by reacting quickly."
            "Avoid long paragraph-style responses."
            "Make it feel spontaneous."
        ),
        llm=model_name,
        verbose=True
    )

    # Agent 2: Formatter
    formatter_agent = Agent(
        role="JSON Formatter",
        goal="Convert the debate into strict JSON format.",
        backstory=(
            "You strictly return only valid JSON in this format:\n"
            "{\n"
            '  "dialogue": [\n'
            '    {"speaker": "A", "text": "..."},\n'
            '    {"speaker": "B", "text": "..."}\n'
            "  ]\n"
            "}\n"
            "No markdown. No explanation."
        ),
        llm=model_name,
        verbose=True
    )

    debate_task = Task(
        description=(
            f"Create a fun and simple debate-style explanation about {topic}. "
            "Use Speaker A and Speaker B format."
        ),
        expected_output="A debate script between Speaker A and Speaker B.",
        agent=debate_agent
    )

    format_task = Task(
        description="Convert the previous debate into strict JSON format.",
        expected_output="Valid JSON with dialogue array.",
        agent=formatter_agent
    )

    crew = Crew(
        agents=[debate_agent, formatter_agent],
        tasks=[debate_task, format_task],
        verbose=True
    )

    return crew.kickoff()