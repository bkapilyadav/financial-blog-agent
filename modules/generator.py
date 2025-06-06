import openai
import os

def generate_blog_content(full_text, url, category):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
You are a financial blog writer. Using the content below, generate a unique, UK English article for a financial blog.

Instructions:
- Include slug: {url.split('//')[-1].split('/')[0]}
- Title (H1, Arial, size 20, bold)
- Summary (160 characters with SEO keywords)
- Category: {category}
- Subheaders (H2, Arial, size 17, bold)
- Symbols like ₹, $, % (no per cent or hyphens)
- Avoid recommendations. Only informative.
- End with a Conclusion + Disclaimer (educational purpose, investment risks)

Content to research:
\"\"\"
{full_text}
\"\"\"
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message["content"]
