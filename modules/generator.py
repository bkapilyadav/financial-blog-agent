import openai
import os
from modules.formatter import format_blog

openai.api_key = os.getenv("OPENAI_API_KEY")  # Streamlit secrets or environment variable

def generate_blog_content(content, url, category):
    title_prompt = f"Give an SEO-friendly blog title based on the following news:\n\n{content[:1000]}"
    slug_prompt = "Convert the following blog title into a lowercase slug URL format (no link, just words, hyphen-separated)."

    title_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": title_prompt}]
    )
    title = title_response.choices[0].message.content.strip()

    slug_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{slug_prompt}\n\n{title}"}]
    )
    slug = slug_response.choices[0].message.content.strip().lower().replace(" ", "-")

    blog_prompt = (
        f"Write a blog in the following format:\n"
        f"a. Include only slug URL words not link specific to the title.\n"
        f"b. Craft a title in Heading 1, Arial font, size 20, bold.\n"
        f"c. Provide a concise summary (160 characters) with keywords.\n"
        f"d. Define the article category: {category}\n"
        f"e. Structure content with subheaders in Heading 2, Arial font, size 17, bold.\n"
        f"f. Add a short conclusion paragraph.\n"
        f"g. Add this Disclaimer strictly:\n"
        f"Disclaimer: This blog has been written exclusively for educational purposes. The securities or companies mentioned are only examples and not recommendations. This does not constitute a personal recommendation or investment advice. It does not aim to influence any individual or entity to make investment decisions. Recipients should conduct their own research and assessments to form an independent opinion about investment decisions. Investments in the securities market are subject to market risks. Read all the related documents carefully before investing.\n\n"
        f"News Content:\n{content[:3000]}"
    )

    blog_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": blog_prompt}],
        temperature=0.7
    )

    blog = blog_response.choices[0].message.content
    return format_blog(slug, title, blog)
