import time
import argparse

class FakeListLLM:
    def __init__(self, responses):
        self.responses = responses
        self.index = 0

    def __call__(self, prompt):
        response = self.responses[self.index % len(self.responses)]
        self.index += 1
        return response

def to_lowercase(text):
    return text.lower()

STOPWORDS = {"the", "is", "in", "and", "to", "a", "of", "on", "for", "with"}

def remove_stopwords(text):
    return " ".join(word for word in text.split() if word not in STOPWORDS)

def summarize(text):
    sentences = text.split(".")
    count = sum(1 for s in sentences if s.strip())
    return f"Summary: The text contains {count} sentence(s)."

def print_flow_diagram():
    print("\nFlow Diagram:")
    print("Input → Lowercase → Remove Stopwords → Summarize → Output\n")


def run_chain(text, trace=False):
    if trace:
        print_flow_diagram()

    steps = [
        ("Lowercase", to_lowercase),
        ("Remove Stopwords", remove_stopwords),
        ("Summarize", summarize),
    ]

    start_time = time.time()
    for name, func in steps:
        print(f"\n--- {name} ---")
        print("Input:", text)
        text = func(text)
        print("Output:", text)

    end_time = time.time()
    print(f"\n Total execution time: {end_time - start_time:.4f} seconds")
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini LangChain-style text processor")
    parser.add_argument("text", type=str, help="Input text to process")
    parser.add_argument("-trace", action="store_true", help="Show flow diagram")
    args = parser.parse_args()

    run_chain(args.text, trace=args.trace)
