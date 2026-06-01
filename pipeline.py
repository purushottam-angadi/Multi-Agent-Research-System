from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain


def run_research_pipe(topic: str)-> dict:
    state={}
    search_agent= build_search_agent()
    scrape_agent= build_scrape_agent()

    print("\n"+"="*50)
    print(f"Step 1: Running research pipeline for topic: {topic}")
    print("\n"+"="*50)
    search_results= search_agent.invoke(
        {
            "messages":[("user", f"Conduct a web search on the topic: {topic} and provide recent and reliable information.")]
        }
    )

    state['search_results']= search_results['messages'][-1].content
    print("\n"+"="*50)
    print("Web Search Results:\n")
    print(state['search_results'])
    print("\n"+"="*50)
    print("\n"+"="*50)
    print("Step 2: Scraping URLs for deeper insights...")
    print("\n"+"="*50)
    scrape_results= scrape_agent.invoke(
        {
            "messages":[("user", f"From the search results of the {topic}, scrape the content of the URLs for deeper insights. Here are the search results:\n{state['search_results'][:800]}")]
        }
    )
    state['scrape_results']= scrape_results['messages'][-1].content

    print("Scrape Results:\n")
    print(state['scrape_results'])
    print("\n"+"="*50)
    print("\n"+"="*50)

    # Step 3: Writing the research report
    print("Step 3: Writing the research report...")
    print("\n"+"="*50)
    research_combined= f"Search Results:\n{state['search_results']}\n\nScrape Results:\n{state['scrape_results']}"
    report= writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined
        }
    )
    state['report']= report
    print("Generated Research Report:\n")
    print(state['report'])
    print("\n"+"="*50)
    print("\n"+"="*50)

    # Step 4: Critiquing the report
    print("Step 4: Critiquing the report...")
    print("\n"+"="*50)
    critique= critic_chain.invoke(
        {
            "report": state['report']
        }
    )
    state['feedback']= critique
    print("Generated Critique:\n")
    print(state['feedback'])
    print("\n"+"="*50)

    return state

if __name__ == "__main__":
    topic= input("Enter a research topic: ")
    run_research_pipe(topic)