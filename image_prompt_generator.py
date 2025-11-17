import boto3
import json

def generate_image_prompt(summary_data):
    client = boto3.client("bedrock-runtime", region_name="ap-south-1")

    prompt = f"""
    Generate an imaginative, vivid, cinematic image prompt based on the following summary.
    The prompt will be used to create an AI visual summary image.

    Summary Data:
    {summary_data}

    Output a single paragraph describing:
    - emotions
    - colors
    - objects
    - scenes
    - mood
    """

    response = client.invoke_model(
        modelId="mistral.mistral-large-2402-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "prompt": prompt,
            "max_tokens": 400
        })
    )

    return response["body"].read().decode("utf-8")
