import streamlit as st
from modules.generator import generate_blog_content
from modules.scraper import scrape_content  # assuming you have scraper.py
import os

st.title("📊 Financial Blog Generator AI")

# Get API key securely (no manual input in the app)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

url = st.text_input("Enter Financial Report URL:")
category = st.selectbox("Select Category", ["Market Update", "Business News", "Stock", "IPO"])

if st.button("Generate Blog"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("🔍 Scraping and analyzing content..."):
            raw_text = scrape_content(url)
        if raw_text:
            with st.spinner("✅ Content scraped. Generating blog with ChatGPT..."):
                try:
                    blog = generate_blog_content(raw_text, url, category)
                    st.markdown(blog, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating blog: {e}")
        else:
            st.error("Failed to scrape content from the URL. Please try a different URL.")
