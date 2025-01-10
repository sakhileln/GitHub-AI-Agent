"""
GitHub Issues AI Agent Module.

This module provides an interactive AI-powered assistant for querying GitHub issues 
from a specified repository. It connects to an AstraDB Vector Store to retrieve 
and store issue data, utilizes OpenAI models for generating responses, 
and includes a tool-based framework for enhanced functionality.

Key Features:
1. AstraDB Integration:
   - Establishes connection to AstraDB using environment variables.
   - Supports updating the vector store with new issues.

2. LangChain-based Tools:
   - Uses LangChain retriever for advanced querying.
   - Leverages OpenAI embeddings for vector search.

3. Interactive Query Interface:
   - Allows users to interactively ask questions about GitHub issues.
   - Real-time query execution via an agent executor.

Environment Variables Required:
- ASTRA_DB_API_ENDPOINT: API endpoint for AstraDB.
- ASTRA_DB_APPLICATION_TOKEN: Authentication token for AstraDB.
- ASTRA_DB_KEYSPACE: Namespace to use in the vector store.

How to Use:
1. Ensure the required environment variables are set.
2. Optionally update the vector store with issues from the specified GitHub repository.
3. Interactively ask questions about GitHub issues through the command line.
4. Type 'q' to exit the interactive loop.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub

from retriever import fetch_github_issues
from summarizer import note_tool

load_dotenv()


def connect_to_vstore():
    """
    Connect to the AstraDB Vector Store using the environment variables for configuration.

    Returns:
        AstraDBVectorStore: An instance of the AstraDB Vector Store connected to the
        specified collection.

    The environment variables required for this function are:
    - `ASTRA_DB_API_ENDPOINT`: The API endpoint for the AstraDB instance.
    - `ASTRA_DB_APPLICATION_TOKEN`: The application token for authentication.
    - `ASTRA_DB_KEYSPACE`: The namespace or keyspace to use for the vector store.
    """
    embeddings = OpenAIEmbeddings()
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore


vstore = connect_to_vstore()
add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in [
    "yes",
    "y",
]

if add_to_vectorstore:
    """
    If the user opts to update the vector store, fetch GitHub issues for the specified repository
    and add them to the vector store after clearing the existing collection.
    """
    owner = "sakhileln"
    repo = "Space-Nomad"
    issues = fetch_github_issues(owner, repo)

    try:
        vstore.delete_collection()
    except:
        pass

    vstore = connect_to_vstore()
    vstore.add_documents(issues)

retriever = vstore.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "github_search",
    "Search for information about github issues. For any questions about github issues, \
    you must use this tool!",
)

prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI()

tools = [retriever_tool, note_tool]
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    """
    Ask the agent questions related to GitHub issues. Use 'q' to exit the loop.

    Args:
        question (str): A user-provided query about GitHub issues.

    Behavior:
        Passes the user's question to the agent executor, which queries the vector store
        and other tools to generate an answer. Outputs the result to the console.
    """
    result = agent_executor.invoke({"input": question})
    print(result["output"])
