import re
from openai import OpenAI

client = OpenAI()

def slugify(title: str) -> str:
    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def generate_blog_content(article_text: str, url: str, category: str) -> str:
    prompt = f"""
You are a professional financial blog writer. Follow these instructions strictly:

a. Create a slug URL from the title words only (no full URL).
b. Craft a blog title in Heading 1 with Arial font, size 20, bold.
c. Provide a concise summary (max 160 characters) with important keywords.
d. Set the article category (e.g., Market Update, Business News, Stock, IPO).
e. Use subheaders in Heading 2 with Arial font, size 17, bold (do NOT include the phrase 'Heading 2' literally).
f. Add a conclusion paragraph summarizing the report.
g. Add the following disclaimer exactly at the end:

Disclaimer: This blog has been written exclusively for educational purposes. The securities or companies mentioned are only examples and not recommendations. This does not constitute a personal recommendation or investment advice. It does not aim to influence any individual or entity to make investment decisions. Recipients should conduct their own research and assessments to form an independent opinion about investment decisions. Investments in the securities market are subject to market risks. Read all the related documents carefully before investing.

Input article text:
{article_text}

Category: {category}

Please generate the formatted blog accordingly.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    blog_text = response.choices[0].message.content

    # Extract title line to create slug
    title_match = re.search(r'^#+\s*(.*)', blog_text, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        slug = slugify(title)
        # Replace slug URL placeholder or insert slug URL line
        if "Slug URL:" in blog_text:
            blog_text = re.sub(r'Slug URL:.*', f'Slug URL: {slug}', blog_text)
        else:
            blog_text = f"Slug URL: {slug}\n\n" + blog_text
    else:
        blog_text = f"Slug URL: could-not-generate\n\n" + blog_text

    return blog_text
