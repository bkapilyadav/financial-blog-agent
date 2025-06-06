import streamlit as st
from modules.scraper import extract_full_text
from modules.generator import generate_blog_content
from modules.formatter import format_for_display
import os

st.set_page_config(page_title="Financial Report Blog AI", layout="centered")

st.title("📊 Financial Blog Generator AI")

# Use API key from env if available, else ask user
openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    openai_key = st.text_input("Enter your OpenAI API key", type="password")
    if not openai_key:
        st.warning("Please enter your OpenAI API key to continue.")
        st.stop()

os.environ["OPENAI_API_KEY"] = openai_key

url = st.text_input("Report URL")
category = st.selectbox("Select Category", ["Stock", "IPO", "Business News", "Finance"])

if st.button("Generate Blog"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        st.info("🔍 Scraping and analyzing content...")
        raw_text = extract_full_text(url)

        if "Error" in raw_text:
            st.error(raw_text)
        else:
            st.success("✅ Content scraped. Generating blog with ChatGPT...")

            article = generate_blog_content(raw_text, url, category)
            formatted = format_for_display(article)

            st.markdown("### ✍️ Final Blog Output")
            st.markdown(formatted, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("✅ Please review manually before copying to Google Docs.")
