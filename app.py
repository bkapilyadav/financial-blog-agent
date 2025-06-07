import streamlit as st
from modules.scraper import scrape_with_playwright
from modules.generator import generate_blog_content
from modules.formatter import format_blog

st.set_page_config(page_title="Financial Blog Generator AI", layout="centered")

st.title("📊 Financial Blog Generator AI")
st.markdown("Enter a financial report URL below:")

url = st.text_input("Report URL")
category = st.selectbox("Select Category", ["Market Update", "Stock", "IPO", "Business News"])

if st.button("Generate Blog"):
    if not url:
        st.error("Please enter a URL.")
    else:
        with st.spinner("Scraping content..."):
            scraped_text = scrape_with_playwright(url)

        if not scraped_text:
            st.error("🚫 Failed to scrape content. Please check the URL.")
        else:
            with st.spinner("Generating blog..."):
                blog = generate_blog_content(scraped_text, url, category)
                formatted_blog = format_blog(blog)

            st.success("✅ Blog generated successfully!")
            st.download_button(
                label="📥 Download Blog as .txt",
                data=formatted_blog,
                file_name="generated_blog.txt",
                mime="text/plain"
            )
            st.text_area("📝 Preview", formatted_blog, height=600)
