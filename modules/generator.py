from openai import OpenAI
import os
import re

def slugify(title):
    # Converts title to lowercase and replaces non-alphanumeric with hyphens
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def generate_blog_content(text, url, category):
    client = OpenAI()

    prompt = f"""
You are a financial blogger.

Write a blog using UK English based on the report below. Follow the structure and rules exactly.

Structure:
1. Slug URL: Use only lowercase title words with hyphens (no actual URL).
2. Title: Use Heading 1, Arial font, size 20, bold.
3. Summary: A 160-character summary with keywords.
4. Category: {category}
5. Body: Structure content using subheaders in Heading 2, Arial font, size 17, bold.
6. Conclusion: Summarise key points.
7. Disclaimer: "This content is for educational purposes only and does not constitute investment advice."

Rules:
- No hyphens in text body (use symbols like ₹, $, %).
- Ensure clarity, structure, and professionalism.
- Output in plain Markdown format with proper spacing and bold elements.

Source Report:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content

    # Extract title (first markdown heading)
    match = re.search(r'^# (.+)', content, re.MULTILINE)
    if match:
        title = match.group(1)
        slug = slugify(title)
        content = f"Slug URL: {slug}\n\n{content}"
    else:
        content = "Slug URL: could-not-generate\n\n" + content

    return content
