import argparse
import json
import os
import random
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryMemory
from langchain_community.llms.fake import FakeListLLM

def generate_response(user_input, history):
    if not history:
        return f"Tell me more about '{user_input}'!"
    previous_user_inputs = [msg["user"] for msg in history if "user" in msg]
    if previous_user_inputs:
        ref_input = random.choice(previous_user_inputs)
        return f"You mentioned '{ref_input}' earlier. Is it related to '{user_input}'?"
    return f"Interesting point about '{user_input}'!"

def load_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_history(file_path, history):
    with open(file_path, "w") as f:
        json.dump(history, f, indent=2)

llm = FakeListLLM(responses=["Summary generated successfully."])

def get_memory(memory_type):
    if memory_type == "buffer":
        return ConversationBufferMemory()
    elif memory_type == "summary":
        return ConversationSummaryMemory(llm=llm)
    else:
        raise ValueError("Invalid memory type. Choose buffer or summary.")

def simulate_chat(memory_type):
    history_file = f"chat_history_{memory_type}.json"
    history = load_history(history_file)
    memory = get_memory(memory_type)

    print(f"\n Using memory type: {memory_type}\n")

    user_inputs = [
        "Travel is a good time for me",
        "My favorite food is the home food",
        "I love automobiles and I'm happy drive all of them.",
        "Which kind of music heals you?",
        "I'm fond of photography."
    ]

    for user_input in user_inputs:
        memory.chat_memory.add_user_message(user_input)
        response = generate_response(user_input, history)
        memory.chat_memory.add_ai_message(response)
        history.append({"user": user_input, "agent": response})
        print(f" You: {user_input}")
        print(f" Agent: {response}\n")

    save_history(history_file, history)
    
    print("-" * 30)
    print(f"Final Memory Content ({memory_type}):\n")
    print(memory.load_memory_variables({}))
    print("-" * 30)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-type", choices=["buffer", "summary"], default="buffer")
    args = parser.parse_args()
    simulate_chat(args.memory_type)