#Om Sai Ram
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from dotenv import load_dotenv
import os
from rich import print
load_dotenv()

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0 Safari/537.36"
            
        }
        response = requests.get(url, timeout=10, headers=headers)

        # Handle non-200 responses gracefully
        if response.status_code != 200:
            return f"Error: Received status code {response.status_code} from {url}"

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
