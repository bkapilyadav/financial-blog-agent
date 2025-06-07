import streamlit as st
from modules.scraper import scrape_content
from modules.generator import generate_blog_content
import os

st.set_page_config(page_title="📊 Financial Blog Generator AI", layout="centered")

st.title("📊 Financial Blog Generator AI")

st.markdown("**Enter a financial report URL below:**")
url = st.text_input("Report URL")

category = st.selectbox("Select Category", ["Market Update", "Business News", "Stock", "IPO"])

if url and category:
    with st.spinner("🔍 Scraping and analyzing content..."):
        raw_text = scrape_content(url)

    if raw_text:
        with st.spinner("✅ Content scraped. Generating blog with ChatGPT..."):
            try:
                blog = generate_blog_content(raw_text, url, category)
                st.markdown(blog, unsafe_allow_html=True)
            except Exception as e:
                st.error("🚫 Failed to generate blog content. Please check your OpenAI key or try again.")
    else:
        st.error("🚫 Failed to scrape content. Please check the URL.")
