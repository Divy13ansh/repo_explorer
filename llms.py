import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import re
load_dotenv()

api_version = os.getenv("AZURE_OPENAI_API_VERSION")  # e.g., "2025-04-14"
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g., "https://subscription_key = os.getenv("AZURE_API_KEY")  # your API key
subscription_key = os.getenv("AZURE_API_KEY")  # your API key
client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # your deployment name


def summarize_file_content(file_content):
    """Use Azure OpenAI to summarize the content of a specific file."""
    prompt = f"Summarize the following code file content in a concise manner(What this file does. and possibly in 2 lines max):\n\n{file_content}"
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an expert software summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500,
    )
    reply = response.choices[0].message.content
    return reply

def file_explanation(file_content):
    """Use Azure OpenAI to summarize the content of a specific file."""
    prompt = f"Provide a concise, clear explanation of the following code file. Describe what each major block/function does and how the code works overall. Keep the explanation short but informative:\n\n{file_content}"
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are an expert software summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1500,
    )
    reply = response.choices[0].message.content
    return reply