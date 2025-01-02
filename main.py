import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain.schema import ChatGeneration
from langchain.schema import BaseMessage, AIMessage
from langchain import hub
from transformers import pipeline

from retriever import fetch_github_issues
from summarizer import note_tool

load_dotenv()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def connect_to_vstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")
    
    ASTRA_DB_KEYSPACE = desired_namespace if desired_namespace else None

    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name="github",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )
    return vstore

vstore = connect_to_vstore()
add_to_vectorstore = input("Do you want to update the issues? (y/N): ").lower() in ["yes", "y"]

if add_to_vectorstore:
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
    "Search for information about github issues. For any questions about github issues, you must use this tool!",
)

tools = [retriever_tool, note_tool]

# Initialize Hugging Face pipeline
llm_pipeline = pipeline("text-generation", model="facebook/opt-350m", device=-1)

# Wrap Hugging Face model into a callable for LangChain
class HuggingFaceAgentWrapper:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def __call__(self, input_text):
        # Ensure input is a string
        if not isinstance(input_text, str):
            if hasattr(input_text, "to_string"):
                input_text = input_text.to_string()
            elif hasattr(input_text, "__str__"):
                input_text = str(input_text)
            else:
                raise TypeError("Input to HuggingFace pipeline must be a string or convertible to string.")

        # Generate response using the pipeline
        response = self.pipeline(input_text, max_length=512, truncation=True, num_return_sequences=1)

        # Ensure response is a string
        generated_text = response[0]["generated_text"]
        if not isinstance(generated_text, str):
            raise TypeError(f"Generated text is expected to be a string, got {type(generated_text)} instead.")

        # Construct the required `message` object for ChatGeneration
        ai_message = AIMessage(content=generated_text)

        # Return as a ChatGeneration instance
        return [ChatGeneration(message=ai_message)]

    def bind_tools(self, tools):
        self.tools = tools
        return self

llm = HuggingFaceAgentWrapper(llm_pipeline)
llm = llm.bind_tools(tools)

prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while (question := input("Ask a question about github issues (q to quit): ")) != "q":
    result = agent_executor.invoke({"input": question})
    print(result["output"])
