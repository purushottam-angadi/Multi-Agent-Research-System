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
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}")

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

       
        main_content = soup.select_one("#mw-content-text, article, main, #content")
        text_source = main_content if main_content else soup

        text = text_source.get_text(separator="\n", strip=True)

        
        return text[:4000] if text else "No readable text found on the page."

    except requests.exceptions.Timeout:
        print(f"Timeout on {url}")
        return "Error: Request timed out while scraping the page."
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return f"Error scraping the web page: {str(e)}"



@tool(return_direct=True)

def write_report(topic: str, research: str) -> str:
    """Generate a structured research report from gathered information."""
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research writer. Write naturally and clearly, but every number, 
date, name, or statistic you use must come from the Research Gathered text — not from your own 
knowledge, even if it's true or well-known.

Keep in mind:
- If the source ties a number to a specific category (e.g. one sub-market, one study, one region), 
keep that number tied to the same category — don't broaden it.
- It's fine to explain, connect ideas, and add flow in your own words — just don't introduce new 
facts, figures, or specifics that aren't in the research.
- If the research is vague on something, it's okay to say so in general terms rather than making 
up a precise number to sound more concrete.
- A Conclusion or takeaways section is fine, but keep it as your own synthesis of what's already 
been said — don't slip in new stats there.

If a point isn't well covered in the research, it's fine to say less about it instead of filling 
the gap yourself."""),
        ("human", """Write a detailed research report on the topic below, using the research provided.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 points, grounded in the Research Gathered)
- Conclusion (your synthesis — no new facts or numbers)

Write naturally, but keep all facts and figures traceable to the research above."""),
    ])
    writer_chain = writer_prompt | llm | StrOutputParser()
    return writer_chain.invoke({"topic": topic, "research": research})


@tool(return_direct=True)
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


@tool(return_direct=True)
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

@tool(return_direct=True)
def fact_check_report(report: str, sources: str) -> ReportVerification:
    """Verify factual claims in a research report against the provided sources."""
    fact_check_prompt = ChatPromptTemplate.from_messages([
    ("system", """You're checking a report against its sources.

The sources are split into "Full Text Sources" (primary evidence) and "Search 
Snippets" (supplementary, lower detail) — prefer the full text when checking a 
claim, and only fall back to a snippet if no fuller text covers that claim.

1. Pick out the 15 most important factual claims in the report — the ones 
with specific numbers, percentages, study names, or dates. Skip generic 
lines like "AI is transforming healthcare" and skip anything from a 
Conclusion or Recommendations section (that's the author's opinion, not 
a fact to check).

2. If there are fewer than 15 real factual claims, just list fewer. 
Don't add filler claims to hit 15.

3. For each claim, check the sources and mark it using EXACTLY one of these 
three words — no other word, no synonyms, no variations:
   - "Verified": the sources say this, with matching numbers/scope
   - "Contradicted": the sources say something different
   - "Unsupported": the sources don't mention this at all

The status field must be one of exactly: Verified, Unsupported, Contradicted.
Do not use "Supported", "Confirmed", "True", "False", "Partially Verified", or 
any other word. Only those three exact strings are valid.

Don't guess. If it's not in the sources, it's Unsupported — even if it 
sounds true or reasonable."""),
    ("human", """Report to verify:
{report}

Sources:
{sources}

Extract every factual claim and check it against the sources above."""),
])
    
    structured_llm = llm.with_structured_output(ReportVerification)
    chain = fact_check_prompt | structured_llm
    return chain.invoke({"report": report, "sources": sources})

    if not result.claims:
        return "No fact-check results available."

    rows = "\n".join(f"| {c.claim} | {c.status} |" for c in result.claims)
    table = (
        f"| Claim | Status |\n|---|---|\n{rows}\n\n"
        f"**Overall accuracy:** {result.overall_accuracy}"
    )
    return table