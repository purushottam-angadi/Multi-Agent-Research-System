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

from rich import print
load_dotenv()


api_key = os.getenv("MISTRAL_API_KEY")
llm = ChatMistralAI(model="mistral-small-2603", temperature=0.7)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)




@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information and return title, url and snippets"""
    results= tavily_client.search(query=query,
       
                                        max_results=5)
    out=[]

    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}")

    return "\n-------\n".join(out)






@tool
def scrape_url(url: str) -> str:
    """Scrape the content of a web page and return clean text content from the given URL for deeper results."""
    try:
        # Add browser-like headers to reduce blocking
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
        response = requests.get(url, timeout=10, headers=headers)

        # Handle non-200 responses gracefully
        if response.status_code != 200:
            return f"Error: Received status code {response.status_code} from {url}"
        
        if "Access Denied" in response.text or "blocked" in response.text.lower():
            return f"Error: Access denied by {url}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "noscript", "iframe"]):
            tag.decompose()

        # Extract clean text
        text = soup.get_text(separator="\n", strip=True)

        # Limit output size for safety
        return text[:3000] if text else "No readable text found on the page."

    except requests.exceptions.Timeout:
        return "Error: Request timed out while scraping the page."
    except requests.exceptions.RequestException as e:
        return f"Error scraping the web page: {str(e)}"



@tool
def write_report(topic: str, research: str) -> str:
    """Generate a structured research report from gathered information."""
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
        ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
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

