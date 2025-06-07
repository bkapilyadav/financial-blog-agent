def format_blog(slug, title, body):
    formatted = f"""
<p><strong>Slug URL:</strong> {slug}</p>
<h1 style='font-family:Arial; font-size:20px; font-weight:bold'>{title}</h1>
{body}
"""
    return formatted
