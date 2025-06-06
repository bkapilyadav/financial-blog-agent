from openai import OpenAI
import os

def generate_blog_content(text, url, category):
    client = OpenAI()  # Automatically picks up OPENAI_API_KEY from environment

    prompt = f"""
You are a professional financial blogger.

Generate a unique, plagiarism-free financial blog article in UK English based on the following content extracted from the URL: {url}.

Category: {category}

Requirements:
- Title in Heading 1, Arial font, size 20, bold.
- Subheaders in Heading 2, Arial font, size 17, bold.
- Include a concise summary of 160 characters with keywords.
- Use ₹, $, and % symbols correctly.
- Avoid hyphens in the body content.
- Include a blog-specific slug URL.
- End with a clear disclaimer that this content is for educational purposes only and does not constitute investment advice.
- Structure the blog professionally with an introduction, well-defined sections, and a conclusion summarising the report.

Content to base the article on:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    article = response.choices[0].message.content
    return article
