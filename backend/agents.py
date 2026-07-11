from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from tools import web_search, scrape_url, write_report, review_report, format_citations, fact_check_report

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(model="mistral-small-2603", temperature=0.2, api_key=api_key)
scrape_agent_llm = ChatMistralAI(
    model="mistral-small-2603",
    temperature=0.0,
    api_key=api_key,
    max_tokens=16000
)

#1st agent for web search
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You must call the web_search tool just once before answering. "
            "Never answer from memory. Never invent URLs, titles, or content. "
            "Every fact in your answer must come directly from the "
            "tool's output. If the tool returns nothing useful, say so explicitly "
            "instead of filling in an answer"
        ),
    )

#2nd agent for web scraping
def build_scrape_agent():
    return create_agent(
        model=scrape_agent_llm,
        tools=[scrape_url],
        system_prompt = (
    "You are a strict URL-scraping executor.\n"
    "You will be given a numbered list of URLs in the user message.\n"
    "Rules:\n"
    "1. Call scrape_url once per URL, in order, using it verbatim.\n"
    "2. Never use example.com or any placeholder/test URL.\n"
    "3. If a call errors, skip it and move to the next URL — no retries, no substitutes.\n"
    "4. Stop as soon as 3 scrapes succeed. If you run out of URLs first, stop there.\n"
    "5. In your final answer, reproduce the FULL text returned by each successful "
    "scrape_url call, verbatim, with no summarizing, shortening, paraphrasing, or "
    "commentary. Do not extract bullet points or 'key ideas' — copy the tool output "
    "character-for-character.\n"
    "6. Separate each source with a header line: '--- SOURCE: <url> ---' followed by "
    "its full raw text.\n"
    "7. Do not add any introduction, explanation, or conclusion of your own — your "
    "final answer should contain nothing except the raw scraped text from each source."
)
    )

def build_writer_agent():
    return create_agent(   
        model=llm,
        tools=[write_report],
        system_prompt=(
            "You are a report-writing agent.\n"
            "Rules:\n"
            "1. Call the write_report tool EXACTLY ONCE per request. Never call it a "
            "second time for any reason — not to retry, refine, expand, or double-check.\n"
            "2. As soon as you receive the tool's output, return it as your final answer. "
            "Do not call any tool again after that.\n"
            "3. Return the tool's output exactly as given. Do not rewrite, summarize, "
            "shorten, or add anything to it.\n"
            "4. Do not add facts, numbers, or commentary of your own before or after "
            "the tool's output."
        ),
    )

def build_critic_agent():
    return create_agent(
        model=llm,
        tools=[review_report],
        system_prompt=(
            "Call review_report exactly once with the given report and return its output as-is."
        ),
    )

def build_citation_agent():
    return create_agent(
        model=llm,
        tools=[format_citations],
        system_prompt= """You are a citation formatting assistant.
You MUST use the format_citations tool to generate citations — never write APA/IEEE citations yourself in plain text.
Given a list of sources, call format_citations with the sources as input, and return exactly what the tool outputs, unmodified."""
    )


def build_fact_checker_agent():
    return create_agent(
        model=llm,
        tools=[fact_check_report],
        system_prompt=(
            "Call fact_check_report exactly once, passing the full report and the full "
            "sources text exactly as given to you — do not summarize or truncate either "
            "before passing them in. Return the tool's output as your final answer, unchanged."
        ),
    )