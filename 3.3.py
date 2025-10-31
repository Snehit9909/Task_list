import random

characters = {
    "Alice": random.choice(["truth", "lie"]),
    "Bob": random.choice(["truth", "lie"]),
    "Charlie": random.choice(["truth", "lie"])
}

history = {
    "Alice": [],
    "Bob": [],
    "Charlie": []
}

def respond(name, question):

    if characters[name] == "truth":
        answer = "yes" if "you lie" not in question.lower() else "no"
    else:
        answer = "no" if "you lie" not in question.lower() else "yes"

    if question in history[name]:
        if characters[name] == "lie":
            answer = "yes" if answer == "no" else "no"
    history[name].append(question)
    return answer

print("Welcome to the Truth & Lie Game!")
print("You meet Alice, Bob, and Charlie. One or more may be lying.")
print("Ask yes/no questions like 'Do you lie?' or 'Is Bob lying?'")
print("Type 'exit' to quit.\n")

while True:
    question = input("Your question: ")
    if question.lower() == "exit":
        break

    for name in characters:
        reply = respond(name, question)
        print(f"{name} says: {reply}")

print("\nGame Over. Here's the truth:")
for name, role in characters.items():
    print(f"{name} was a {role}-teller.")
