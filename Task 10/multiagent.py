from langchain_core.tools import Tool

def analyst_agent(_):
    return (
        "Proposed Schedule:\n"
        "9:00 AM - Introduction to AI\n"
        "10:00 AM - Machine Learning Basics\n"
        "12:00 PM - Lunch Break\n"
        "1:00 PM - Hands-on with Python\n"
        "3:00 PM - Deep Learning Overview\n"
        "4:30 PM - Q&A and Wrap-Up"
    )

def critic_agent(context: str):
    return (
        "Schedule is solid but needs breaks between sessions.\n"
        "Add an opening keynote and a closing networking session."
    )

def summarizer_agent(context: str):
    return (
        "Final Schedule:\n"
        "9:00 AM - Keynote: The Future of AI\n"
        "9:30 AM - Introduction to AI Concepts\n"
        "10:30 AM - Coffee Break\n"
        "10:45 AM - Machine Learning Basics\n"
        "12:00 PM - Lunch Break\n"
        "1:00 PM - Hands-on with Python for AI\n"
        "3:00 PM - Deep Learning Overview\n"
        "4:15 PM - Networking & Q&A Session\n"
        "5:00 PM - Closing Remarks"
    )

analyst_tool = Tool(
    name="Analyst",
    func=analyst_agent,
    description="Proposes initial AI workshop schedule."
)

critic_tool = Tool(
    name="Critic",
    func=critic_agent,
    description="Provides critique or suggestions to improve the workshop."
)

summarizer_tool = Tool(
    name="Summarizer",
    func=summarizer_agent,
    description="Synthesizes inputs into a polished final schedule."
)

def multi_agent_simulation():
    conversation_history = []
    analyst_output = analyst_tool.run("")
    conversation_history.append(("Analyst", analyst_output))

    critic_output = critic_tool.run(analyst_output)
    conversation_history.append(("Critic", critic_output))

    summarizer_input = "\n\n".join(f"{role}: {msg}" for role, msg in conversation_history)
    summarizer_output = summarizer_tool.run(summarizer_input)
    conversation_history.append(("Summarizer", summarizer_output))

    for role, msg in conversation_history:
        print(f"{role}:\n{msg}\n")
    print("Final Workshop Plan \n")
    print(summarizer_output)

if __name__ == "__main__":
    multi_agent_simulation()
