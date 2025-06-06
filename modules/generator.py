from openai import OpenAI
import os
import re

def slugify(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def generate_blog_content(text, url, category):
    client = OpenAI()

    prompt = f"""
You are a financial blog writer.

Write a unique and plagiarism-free blog article in UK English using the content below.

Rules:
- Title in H1 format (Heading 1), Arial, size 20, bold
- Subheaders in H2 (Heading 2), Arial, size 17, bold
- Summary in ≤160 characters
- Category should be "Market Update"
- Do not write "Body:" anywhere
- Do not include any URLs
- Use ₹, $, % symbols correctly
- Avoid hyphens in the article body
- End with this disclaimer (exactly as given):
---
This blog has been written exclusively for educational purposes. The securities or companies mentioned are only examples and not recommendations. This does not constitute a personal recommendation or investment advice. It does not aim to influence any individual or entity to make investment decisions. Recipients should conduct their own research and assessments to form an independent opinion about investment decisions.

Investments in the securities market are subject to market risks. Read all the related documents carefully before investing.
---

Source content:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content

    # Extract title to create slug
    match = re.search(r'^# (.+)', content, re.MULTILINE)
    if match:
        title = match.group(1)
        slug = slugify(title)
        content = f"Slug URL: {slug}\n\n{content}"
    else:
        content = "Slug URL: could-not-generate\n\n" + content

    # Override category to "Market Update"
    content = re.sub(r'(?i)(\*\*Category:\*\*).*', r'**Category:** Market Update', content)

    return content
