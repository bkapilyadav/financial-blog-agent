import openai
import re
import os

# Load OpenAI API key securely from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def slugify(title):
    slug = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    slug = re.sub(r'\s+', '-', slug.strip().lower())
    return slug

def generate_blog_content(text, source_url, category):
    prompt = f"""
You are an expert UK-based financial journalist.

Write a professional and unique financial blog article based on the following report content:

{text}

Follow these formatting rules:

a. Generate a slug URL using only lowercase words from the title, separated by hyphens. Do NOT include the source URL.
b. Craft a clear and engaging title (Heading 1, Arial, size 20, bold).
c. Provide a concise summary (max 160 characters) including keywords.
d. Category should be: {category}
e. Structure blog content using Heading 2 for subheaders (Arial, size 17, bold) — include 3 to 5 such sections.
f. Add a final paragraph titled 'Conclusion' with a summary.
g. Add this exact disclaimer at the end:

Disclaimer: This blog has been written exclusively for educational purposes. The securities or companies mentioned are only examples and not recommendations. This does not constitute a personal recommendation or investment advice. It does not aim to influence any individual or entity to make investment decisions. Recipients should conduct their own research and assessments to form an independent opinion about investment decisions. Investments in the securities market are subject to market risks. Read all the related documents carefully before investing.

Important instructions:
- Use UK English
- Use symbols like ₹, $ and % instead of words
- Do not use hyphens in the main body content
- Output only the clean final formatted article as plain text
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    result = response.choices[0].message.content.strip()

    # Extract title and slugify
    title_match = re.search(r'^(.+)', result)
    title = title_match.group(1).strip() if title_match else None
    slug_url = slugify(title) if title else "could-not-generate"

    blog_output = f"""Final Blog Output

Slug URL: {slug_url}

{result}
"""
    return blog_output
