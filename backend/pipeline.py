# from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain

#THIS IS USING LANGCHAIN 
# def run_research_pipe(topic: str)-> dict:
#     state={}
#     search_agent= build_search_agent()
#     scrape_agent= build_scrape_agent()

#     print("\n"+"="*50)
#     print(f"Step 1: Running research pipeline for topic: {topic}")
#     print("\n"+"="*50)
#     search_results= search_agent.invoke(
#         {
#             "messages":[("user", f"Conduct a web search on the topic: {topic} and provide recent and reliable information.")]
#         }
#     )

#     state['search_results']= search_results['messages'][-1].content
#     print("\n"+"="*50)
#     print("Web Search Results:\n")
#     print(state['search_results'])
#     print("\n"+"="*50)
#     print("\n"+"="*50)
#     print("Step 2: Scraping URLs for deeper insights...")
#     print("\n"+"="*50)
#     scrape_results= scrape_agent.invoke(
#         {
#             "messages":[("user", f"From the search results of the {topic}, scrape the content of the URLs for deeper insights. Here are the search results:\n{state['search_results'][:800]}")]
#         }
#     )
#     state['scrape_results']= scrape_results['messages'][-1].content

#     print("Scrape Results:\n")
#     print(state['scrape_results'])
#     print("\n"+"="*50)
#     print("\n"+"="*50)

#     # Step 3: Writing the research report
#     print("Step 3: Writing the research report...")
#     print("\n"+"="*50)
#     research_combined= f"Search Results:\n{state['search_results']}\n\nScrape Results:\n{state['scrape_results']}"
#     report= writer_chain.invoke(
#         {
#             "topic": topic,
#             "research": research_combined
#         }
#     )
#     state['report']= report
#     print("Generated Research Report:\n")
#     print(state['report'])
#     print("\n"+"="*50)
#     print("\n"+"="*50)

#     # Step 4: Critiquing the report
#     print("Step 4: Critiquing the report...")
#     print("\n"+"="*50)
#     critique= critic_chain.invoke(
#         {
#             "report": state['report']
#         }
#     )
#     state['feedback']= critique
#     print("Generated Critique:\n")
#     print(state['feedback'])
#     print("\n"+"="*50)

#     return state

# if __name__ == "__main__":
#     topic= input("Enter a research topic: ")
#     run_research_pipe(topic)


#  USING LANGGRAPH

from agents import (
    build_search_agent,
    build_scrape_agent,
    build_writer_agent,
    build_critic_agent,
    build_citation_agent,
)
from langgraph.graph import StateGraph, END, START
from typing import TypedDict


class ResearchState(TypedDict):
    topic: str
    search_results: str
    scrape_results: str
    report: str
    feedback: str
    fact_check: str
    citations: str


def search_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("Step 1: Running search agent...")
    agent = build_search_agent()
    result = agent.invoke({
        "messages": [("user", f"Conduct a web search on the topic: {state['topic']} and provide recent and reliable information.")]
    })
    state["search_results"] = result["messages"][-1].content
    return state


def scrape_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("Step 2: Running scrape agent...")
    agent = build_scrape_agent()
    result = agent.invoke({
        "messages": [("user", f"From the search results of {state['topic']}, scrape the content of the URLs for deeper insights.\n{state['search_results'][:800]}")]
    })
    state["scrape_results"] = result["messages"][-1].content
    return state


def writer_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("Step 3: Generating research report...")
    agent = build_writer_agent()
    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Scrape Results:\n{state['scrape_results']}"
    )
    result = agent.invoke({
        "messages": [("user", f"Write a detailed research report on {state['topic']} using this data: {research_combined}")]
    })
    state["report"] = result["messages"][-1].content
    return state


def critic_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("Step 4: Reviewing report...")
    agent = build_critic_agent()
    result = agent.invoke({
        "messages": [("user", f"Review the following research report and provide feedback:\n{state['report']}")]
    })
    state["feedback"] = result["messages"][-1].content
    return state



def citation_node(state: ResearchState):
    print("\n" + "=" * 50)
    print("Step 6: Generating citations...")
    agent = build_citation_agent()
    result = agent.invoke({
        "messages": [("user", f"Format the following sources into APA and IEEE style:\n{state['search_results']}")]
    })
    state["citations"] = result["messages"][-1].content
    return state


# Build graph
graph_builder = StateGraph(ResearchState)

graph_builder.add_node("search", search_node)
graph_builder.add_node("scrape", scrape_node)
graph_builder.add_node("writer", writer_node)
graph_builder.add_node("critic", critic_node)
# graph_builder.add_node("fact_checker", fact_checker_node)
graph_builder.add_node("citations", citation_node)

graph_builder.add_edge(START, "search")
graph_builder.add_edge("search", "scrape")
graph_builder.add_edge("scrape", "writer")
graph_builder.add_edge("writer", "critic")
graph_builder.add_edge("critic", "citations")
graph_builder.add_edge("citations", END)

app = graph_builder.compile()


def run_pipeline(topic: str) -> dict:
    result = app.invoke({"topic": topic})
    return {
        "topic": result["topic"],
        "report": result["report"],
        "feedback": result["feedback"],
        "citations": result["citations"],
    }
