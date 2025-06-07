import openai
import re
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def generate_blog_content(raw_text, url, category):
    prompt = f"""
You are a financial blog writer. Based on the article content below, generate a well-structured blog with the following format:

a. Slug URL: Only lowercase words from the title, hyphen-separated.
b. Title: Use Heading 1, Arial font, size 20, bold.
c. Summary: Max 160 characters with financial keywords.
d. Category: Use the category input provided.
e. Use structured subheaders as Heading 2, Arial font, size 17, bold.
f. Add a conclusion summarizing the implications.
g. Add the mandatory disclaimer at the end:

"This blog has been written exclusively for educational purposes. The securities or companies mentioned are only examples and not recommendations. This does not constitute a personal recommendation or investment advice. It does not aim to influence any individual or entity to make investment decisions. Recipients should conduct their own research and assessments to form an independent opinion about investment decisions. Investments in the securities market are subject to market risks. Read all the related documents carefully before investing."

ARTICLE:
{raw_text}
CATEGORY: {category}
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    blog_text = response.choices[0].message.content
    return blog_text
