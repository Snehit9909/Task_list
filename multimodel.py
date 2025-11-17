import json
from extract_data import extract_key_data
from summarize_and_classify import summarize_and_classify
from image_prompt_generator import generate_image_prompt

def load_raw_reviews(path="input.txt"):
    with open(path, "r") as f:
        return f.read()

def main():
    print(" Loading raw review text...")
    raw_text = load_raw_reviews()

    print("\n Step 1: Extracting key data using Titan...")
    extracted = extract_key_data(raw_text)
    print("Extracted Data:", extracted, "\n")

    print(" Step 2: Summarizing and classifying sentiment using Claude...")
    summary = summarize_and_classify(extracted)
    print("Summary + Sentiment:", summary, "\n")

    print(" Step 3: Generating visual summary prompt using Mistral...")
    visual_prompt = generate_image_prompt(summary)
    print("Visual Summary Prompt:", visual_prompt, "\n")

    print(" Workflow completed successfully!")

if __name__ == "__main__":
    main()
