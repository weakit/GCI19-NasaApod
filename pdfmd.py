import markdown as md
from weasyprint import HTML, CSS
import os
import time

CSS_ = """body { font-family: sans-serif !important }
img { max-width: 100%; }
p { text-align: justify; hyphens: auto;}
"""


def mark(data):
    return f"""### {data['date']}
# {data['title']}
![{data['title']}]({data['image_url']})
### {data['credits']}
{data['summary']}
"""


def make_pdf(s):
    t = f"PDFs/{str(time.time()).replace('.', '')}.pdf"
    if not os.path.isdir('PDFs'):
        os.mkdir('PDFs')
    HTML(string=s).write_pdf(t, stylesheets=[CSS(string=CSS_)])
    return t


def pdf(d):
    return make_pdf(md.markdown(mark(d)))
