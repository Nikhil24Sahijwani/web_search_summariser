from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_community.document_loaders import WebBaseLoader

def summarize_content(url):
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Define the Summarize Chain
    template = """Provide a concise summary of the following website content in under 50 words, focusing on its main purpose, target audience, and unique features:
                    "{text}"
                    CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(template)
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

    # Invoke Chain
    response = stuff_chain.invoke(docs)
    return response["output_text"], url
