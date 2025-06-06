import markdown2

def format_for_display(content):
    """
    Converts raw markdown/structured text into HTML for Streamlit.
    """
    html_content = markdown2.markdown(content)
    return html_content
