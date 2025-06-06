import openai
import re

def slugify(title):
    # Convert title to slug URL format: lowercase, remove special chars, replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def generate_blog_content(article_text, url, category):
    # Extract title keywords for slug generation
    prompt = f"""
You are a professional financial blog writer. Based on the article content provided below, generate a blog in UK English with the following format and rules:

1. Do not mention the word "Heading 1" or "Heading 2" in the output.
2. Use proper formatting as per instructions without labels like "Body", "Title", etc.
3. Do not repeat any line or section.
4. Use % instead of 'percent', ₹ or $ instead of 'rupees' or 'dollars'. Avoid hyphens in the body content.

Use this format strictly:

a. Slug URL — only use lowercase words from the blog title separated by hyphens.
b. Title — format as: Heading 1, Arial font, size 20, bold.
c. Summary — one sentence under 160 characters with keywords.
d. Category — use the exact user-provided category, or default to "Market Update".
e. Use clear subheaders — format as Heading 2, Arial font, size 17, bold.
f. Conclusion — a short summary section.
g. Add the mandatory Disclaimer at the end exactly as below.

Disclaimer: This blog has been written exclusively for educational purposes. The securities or companies mentioned are only examples and not recommendations. This does not constitute a personal recommendation or investment advice. It does not aim to influence any individual or entity to make investment decisions. Recipients should conduct their own research and assessments to form an independent opinion about investment decisions. Investments in the securities market are subject to market risks. Read all the related documents carefully before investing.

--- Begin article content ---

{article_text}

--- End article content ---
"""

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    blog_text = response['choices'][0]['message']['content']

    # Try extracting the blog title for slug generation
    title_match = re.search(r'Title:\s*(.*)', blog_text)
    if title_match:
        title = title_match.group(1).strip()
        slug = slugify(title)
        blog_text = re.sub(r'Slug URL:.*', f'Slug URL: {slug}', blog_text)
    else:
        blog_text = re.sub(r'Slug URL:.*', f'Slug URL: could-not-generate', blog_text)

    return blog_text
