#Om Sai Ram
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import httpx
from rich import print
load_dotenv()


api_key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(model="mistral-small-2603", temperature=0.1)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information and return title, url and snippets"""
    results = tavily_client.search(query=query, max_results=5, search_depth="advanced", include_answer=True)

    out = []
    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:500]}")

    sources_text = "\n-------\n".join(out)
    return sources_text  






@tool
def scrape_url(url: str) -> str:
    """Scrape the content of a web page and return clean text content from the given URL for deeper results."""
    try:

        headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/"
    }
        print(f"🔍 Attempting scrape: {url}")
        response = requests.get(url, timeout=20, headers=headers)
        print(f"Status code: {response.status_code}")
      
        if response.status_code != 200:
            print(f"Non-200 response, skipping")
            return f"Error: Received status code {response.status_code} from {url}"
        
        if "Access Denied" in response.text or "blocked" in response.text.lower():
            print(f"Access denied by {url}")
            return f"Error: Access denied by {url}"

        soup = BeautifulSoup(response.text, "html.parser")

       
        for tag in soup(["script", "style", "nav", "footer", "noscript", "iframe"]):
            tag.decompose()

       
        text = soup.get_text(separator="\n", strip=True)

        
        return text[:8000] if text else "No readable text found on the page."

    except requests.exceptions.Timeout:
        print(f"Timeout on {url}")
        return "Error: Request timed out while scraping the page."
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return f"Error scraping the web page: {str(e)}"




@tool
def write_report(topic: str, research: str) -> str:
    """Generate a structured research report from gathered information."""
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. You must write ONLY using facts explicitly present in the Research Gathered text provided to you. You are strictly forbidden from adding facts, statistics, dates, examples, or claims from your own general knowledge, even if they are true or commonly known. If the research is thin on a point, say less about it rather than filling the gap yourself."),
        ("human", """Write a detailed research report on the topic below, using ONLY the research provided. Do not introduce any external facts.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points, each traceable to something in the Research Gathered)
- Conclusion

Every factual sentence must be derivable from the Research Gathered above. If you're unsure whether something is in the source, leave it out."""),
    ])
    writer_chain = writer_prompt | llm | StrOutputParser()
    return writer_chain.invoke({"topic": topic, "research": research})


@tool
def review_report(report: str) -> str:
    """Critique a research report and provide feedback."""
    critic_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a balanced and supportive research reviewer. Acknowledge strengths generously and keep improvement suggestions brief and focused."),
        ("human", """Review the research report below and evaluate it fairly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
    ])
    critic_chain = critic_prompt | llm | StrOutputParser()
    return critic_chain.invoke({"report": report})


@tool
def format_citations(sources: str) -> str:
    """Format sources into APA and IEEE style citations."""
    citation_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a citation formatter. Format references in APA and IEEE style."),
    ("human", """Format the following sources into APA and IEEE style:

    Sources:
    {sources}

    Respond with:
    APA:
    ...
    IEEE:
     ..."""),
    ])

    citation_chain = citation_prompt | llm | StrOutputParser()
    return citation_chain.invoke({"sources": sources})



from pydantic import BaseModel, Field
from typing import List, Literal

class ClaimVerification(BaseModel):
    claim: str
    status: Literal["Verified", "Unsupported", "Contradicted"]

class ReportVerification(BaseModel):
    claims: List[ClaimVerification]
    overall_accuracy: Literal["High", "Medium", "Low"]

@tool
def fact_check_report(report: str, sources: str) -> ReportVerification:
    """Verify factual claims in a research report against the provided sources."""
    fact_check_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a rigorous fact-checker. The 'sources' text contains content 
gathered from research scraped pages. Identify only the MOST IMPORTANT, SPECIFIC, and CHECKABLE factual claims 
in the report — a maximum of 15 claims total. Prioritize claims with concrete numbers, names, dates, or events 
over vague/general statements. Skip filler sentences, transitions, and claims that are too generic to verify 
(e.g. "X is important" or "X continues to grow").
For each claim you select:
- Check whether the sources support or contradict it.
- If supported → Verified.
- If contradicted → Contradicted.
- If nothing in the sources addresses it → Unsupported. Do not guess or use outside knowledge."""),
("human", """Report to verify:
{report}

Sources:
{sources}

Extract every factual claim and check it against the sources above."""),
    ])
    structured_llm = llm.with_structured_output(ReportVerification)
    chain = fact_check_prompt | structured_llm
    return chain.invoke({"report": report, "sources": sources})