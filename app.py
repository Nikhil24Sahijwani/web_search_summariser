import streamlit as st
from googlesearch import search
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
import os

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Function to get unique top links
def get_unique_websites(query, num_results=10):

    # Using set to avoid duplicates
    seen_url = set()

    # List containing the unique SearchResult objects
    unique = []
    
    # Iterating over to find the unique SearchResult objects
    for i in search(query, num_results=num_results, advanced=True):
        if i.url not in seen_url:
            seen_url.add(i.url)
            unique.append(i)

            if len(unique) == 5:
                    break
            
    # Returning the list of unique SearchResult objects
    return unique

# Streamlit interface
st.title('Web Search Summarizer')

# User input
query = st.text_input('Enter your search query:')

if st.button('Search'):
    if query:
        st.write(f'Searching for: {query}')
        results = get_unique_websites(query)
        
        # Summarize content from the links
        for i in results:
            loader = WebBaseLoader(i.url)
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
            st.subheader(i.title)
            st.write('Summary:')
            st.write(response["output_text"])
            st.write('Link:',i.url)
            # st.write(i.url)
            st.write('---') 
    else:
        st.write('Please enter a query.')

