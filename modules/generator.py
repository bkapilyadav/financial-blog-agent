from openai import OpenAI
import os
import re

def slugify(title):
    # Lowercase, remove special characters, replace spaces with hyphens
    return "www.finblog.com/" + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def generate_blog_content(text, url, category):
    client = OpenAI()

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

    # Try to extract the title (assumes it's first line starting with "# ")
    title_match = re.search(r'^# (.+)', article, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
        slug_url = slugify(title)
        article = f"**Slug URL:** {slug_url}\n\n" + article
    else:
        article = "**Slug URL:** [Could not auto-generate]\n\n" + article

    return article
