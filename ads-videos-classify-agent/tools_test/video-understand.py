import boto3

client = boto3.client("bedrock-runtime")

with open("../test_data/347302344741888073_cut_output.mp4", "rb") as file:
    media_bytes = file.read()

PROMPT="""Please analyze the following video content and identify:
What is the main product or service being showcased
Key features and functionalities of the product
Main selling points and advantages emphasized by the presenter
Who appears to be the target audience
Pricing information and purchasing methods
Brand or manufacturer of the product
Please provide a concise analysis that helps me understand the essence and value proposition of this product. If there are any unique selling points or special offers mentioned, please highlight those as well."

This prompt should help you get a clear understanding of what's being sold in the video you're watching"""
messages = [
    {
        "role": "user",
        "content": [
            {"video": {"format": "mp4", "source": {"bytes": media_bytes}}},
            {"text": PROMPT},
        ],
    }
]

response = client.converse(modelId="us.amazon.nova-lite-v1:0", messages=messages)
print(response["output"]["message"]["content"][0]["text"])