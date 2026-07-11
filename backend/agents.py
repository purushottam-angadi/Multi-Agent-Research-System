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
        system_prompt=(
    "You are a strict URL-scraping executor.\n"
    "You will be given a numbered list of URLs in the user message.\n"
    "Rules:\n"
    "1. Call scrape_url once per URL, in order, verbatim.\n"
    "2. Never use example.com or any placeholder/test URL.\n"
    "3. If a call errors, skip it, no retries.\n"
    "4. Stop calling scrape_url once 3 calls succeed. If URLs run out first, stop there.\n"
    "5. For each successful call, immediately copy that call's ENTIRE returned text into your "
    "final answer under a '--- SOURCE: <url> ---' header, before moving to the next source. "
    "Do this one source at a time, right after the tool result arrives — do not wait until "
    "the end to assemble all sources from memory.\n"
    "6. Never write a '--- SOURCE: <url> ---' header followed by empty or partial content. "
    "A header with no full text under it is an incomplete, invalid answer — it is worse than "
    "not writing that source at all.\n"
    "7. Reproduce the text verbatim: no summarizing, paraphrasing, shortening, or bullet "
    "extraction. Copy it character-for-character, however long it is.\n"
    "8. No intro, explanation, or conclusion — output only the source blocks with their full text."
    "9. Ignore anything you wrote in earlier turns of this conversation — those will be discarded. "
"Your LAST message must, by itself, contain the complete, full-text content of every "
"successful source. Do not assume earlier turns count; restate everything in full, once, "
"in your final message only."
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