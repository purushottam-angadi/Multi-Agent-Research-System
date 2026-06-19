from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url, write_report, review_report, format_citations
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(model="mistral-small-2603", temperature=0.7, api_key=api_key)

#1st agent for web search
def build_search_agent():
     return create_agent(
        model=llm,
        tools=[web_search],
     )

#2nd agent for web scraping
def build_scrape_agent():
        return create_agent(
            model=llm,
            tools=[scrape_url],
        )

def build_writer_agent():
    return create_agent(   # 👈 changed
        model=llm,
        tools=[write_report],
    )

def build_critic_agent():
    return create_agent(   # 👈 changed
        model=llm,
        tools=[review_report],
    )

def build_citation_agent():
    return create_agent(
        model=llm,
        tools=[format_citations],
    )

