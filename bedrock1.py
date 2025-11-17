import boto3
import json
import pandas as pd
from textblob import TextBlob
import csv

REGION = "ap-south-1"

MODELS = [
    "amazon.titan-text-express-v1",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "meta.llama3-8b-instruct-v1:0"
]

def load_prompts(path="prompts.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

def invoke_model(model_id, prompt):
    if model_id.startswith("amazon.titan"):
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 250,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9
            }
        })

    elif model_id.startswith("anthropic.claude"):
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ],
            "max_tokens": 512,
            "temperature": 0.5
        })

    elif model_id.startswith("meta.llama3"):
        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": 250,
            "temperature": 0.7,
            "top_p": 0.9
        })

    else:
        raise ValueError(f"Unsupported model format for {model_id}")

    response = bedrock.invoke_model(
        modelId=model_id,
        body=body,
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    if model_id.startswith("amazon.titan"):
        if "outputText" in result:
            return result["outputText"]
        elif "results" in result and len(result["results"]) > 0:
            return result["results"][0].get("outputText", "")
        else:
            return ""

    elif model_id.startswith("anthropic.claude"):
        return result["content"][0]["text"]

    elif model_id.startswith("meta.llama3"):
        return (
            result.get("generation")
            or result.get("results", [{}])[0].get("outputText", "")
        )

    return ""

def evaluate_metrics(text):
    sentiment = TextBlob(text).sentiment.polarity
    length = len(text.split())  
    return {
        "response_length": length,
        "sentiment_score": sentiment,
        "factual_accuracy": "N/A" 
    }

def run_evaluation():
    prompts = load_prompts()
    all_results = []

    for model in MODELS:
        for prompt in prompts:
            print(f"Invoking {model} with prompt: {prompt}")

            try:
                response_text = invoke_model(model, prompt)
            except Exception as e:
                response_text = f"ERROR: {str(e)}"

            metrics = evaluate_metrics(response_text)

            all_results.append({
                "model": model,
                "prompt": prompt,
                "response": response_text,
                **metrics
            })

    df = pd.DataFrame(all_results)
    df["response"] = df["response"].str.replace("\n", " ", regex=False)
    df.to_csv(
        "results.csv",
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )


    print("\n Saved results to results.csv")


if __name__ == "__main__":
    run_evaluation()
