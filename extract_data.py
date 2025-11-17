import boto3
import json

def load_raw_reviews(path="input.txt"):
    with open(path, "r") as f:
        return f.read()

def extract_key_data(raw_text):
    client = boto3.client("bedrock-runtime", region_name="ap-south-1")

    prompt = f"""
    Extract structured data from the following review text.
    Output JSON with fields:
    - features
    - pros
    - cons
    - user_sentiment_clues
    - keywords

    Text:
    {raw_text}
    """

    body = {
        "inputText": prompt
    }

    response = client.invoke_model(
        modelId="amazon.titan-text-lite-v1",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    output = response["body"].read().decode("utf-8")
    return output


def summarize_and_classify(structured_data):
    client = boto3.client("bedrock-runtime", region_name="ap-south-1")

    prompt = f"""
    Summarize the extracted review data and classify sentiment.
    Output JSON with:
    - summary
    - sentiment (positive/negative/neutral)
    - reasoning

    Data:
    {structured_data}
    """

    body = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 750
    }

    response = client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    output = response["body"].read().decode("utf-8")
    return output


def generate_image_prompt(summary_data):
    client = boto3.client("bedrock-runtime", region_name="ap-south-1")

    prompt = f"""
    Create a vivid cinematic image prompt representing the following review summary.
    The prompt must describe:
    - emotions
    - scene details
    - visual style
    - colors
    - mood

    Summary:
    {summary_data}
    """

    body = {
        "prompt": prompt,
        "max_tokens": 300
    }

    response = client.invoke_model(
        modelId="mistral.mistral-large-2402-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    output = response["body"].read().decode("utf-8")
    return output


def main():
    print("Loading raw text...\n")
    raw_text = load_raw_reviews()

    print("Step 1: Extracting key data (Titan)...")
    extracted = extract_key_data(raw_text)
    print("\nExtracted Data:\n", extracted, "\n")

    print("Step 2: Summarizing + sentiment (Claude)...")
    summary = summarize_and_classify(extracted)
    print("\nSummary & Sentiment:\n", summary, "\n")

    print("Step 3: Generating image prompt (Mistral)...")
    image_prompt = generate_image_prompt(summary)
    print("\nImage Prompt:\n", image_prompt, "\n")

    print("Workflow completed successfully!")

if __name__ == "__main__":
    main()
