import streamlit as st
from search_utils import get_unique_websites
from summarizer import summarize_content
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

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
            summary, url = summarize_content(i.url)
            st.subheader(i.title)
            st.write('Summary:')
            st.write(summary)
            st.write('Link:', url)
            st.write('---') 
    else:
        st.write('Please enter a query.')
