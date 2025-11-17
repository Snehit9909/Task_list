import boto3
import json

def summarize_and_classify(structured_data):
    client = boto3.client("bedrock-runtime", region_name="ap-south-1")

    prompt = f"""
    Summarize the extracted product review data and classify sentiment.
    Output JSON with:
    - summary
    - sentiment (positive/negative/neutral)
    - reasoning

    Data:
    {structured_data}
    """

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 800,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    output = response["body"].read().decode("utf-8")
    return output
    
