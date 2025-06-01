from dotenv import load_dotenv 
import os, requests
from openai import OpenAI

load_dotenv()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def run_web_request(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch the URL: {url}, Status Code: {response.status_code}")
        sys.exit(1)
    return response.text


def init_llm():
    llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return llm

def run_extraction_prompt(prompt, llm):
    response = llm.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
            "role": "system", \
            "content":
            "You are a helpful data extraction assistent,\
            tasked with extracting data from HTML documents and converting into a given format."
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def run_summary_prompt(prompt, llm):
    response = llm.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
            "role": "system", \
            "content":
            "You are a helpful data summarization assistent,\
            tasked with summarizing data from JSON documents and \
            offering the best result that matches a user's request."
            },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()