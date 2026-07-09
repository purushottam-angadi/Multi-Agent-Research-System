from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from tools import web_search, scrape_url, write_report, review_report, format_citations, fact_check_report

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(model="mistral-small-2603", temperature=0.2, api_key=api_key)

#1st agent for web search
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You must call the web_search tool at least once before answering. "
            "Never answer from memory. Never invent URLs, titles, or content. "
            "Every fact and every URL in your answer must come directly from the "
            "tool's output. If the tool returns nothing useful, say so explicitly "
            "instead of filling in an answer."
        ),
    )

#2nd agent for web scraping
def build_scrape_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt = (
       "You are a strict URL-scraping executor.\n"
"You will be given a numbered list of URLs in the user message.\n"
"Rules:\n"
"1. Call scrape_url once per URL, in order, using it verbatim.\n"
"2. Never use example.com or any placeholder/test URL.\n"
"3. If a call errors, skip it and move to the next URL — no retries, no substitutes.\n"
"4. Stop as soon as 3 scrapes succeed. If you run out of URLs first, stop there.\n"
"5. Report back only the content from the successful scrapes."
    ) 
    )


def build_writer_agent():
    return create_agent(   
        model=llm,
        tools=[write_report],
    )

def build_critic_agent():
    return create_agent( 
        model=llm,
        tools=[review_report],
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
            "You are a fact-checking agent.\n"
            "Rules:\n"
            "1. Always call the fact_check_report tool to verify claims.\n"
            "2. Never invent or assume facts — only use the tool output.\n"
            "3. Present the tool’s results in a clear tabular format.\n"
            "   - Use Markdown tables with headers.\n"
            "   - Each row should represent one claim and its verification status.\n"
            "   - Include columns like: Claim | Status | Source.\n"
            "4. If the tool returns nothing, explicitly say 'No fact-check results available'."
        ),
    )