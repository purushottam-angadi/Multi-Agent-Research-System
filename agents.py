from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatMistralAI(model="mistral-small-2603", temperature=0.7)

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

# create a writer chain using modern LCEL pipeline which 
# takes all the research and writes a full report and then a writer chain

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

writer_chain= writer_prompt | llm | StrOutputParser()


#critic chain to review the report and suggest improvements

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()