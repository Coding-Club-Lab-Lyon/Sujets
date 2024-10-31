#!/usr/bin/env python3
from compileall import compile_path
import io
import os
import markdown
import json
import re
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
from reportlab.pdfbase.ttfonts import TTFont
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from time import sleep
from weasyprint import HTML
from PyPDF2 import PdfWriter, PdfReader, PdfMerger

if len(sys.argv) < 4:
    print("Usage: python3 cc_subjects.py <file> <title> <version> <campus>")
    exit(1)

compile_file = sys.argv[1]
export_dir = "/".join(compile_file.split("/")[:-1])
project_title = sys.argv[2]
project_version = sys.argv[3][:10]
project_campus = sys.argv[4]


def str_to_snake_case(str):
    str = str.title().replace(" ", "-")
    str = re.sub('([^\w-])', '_', str)
    str = re.sub('^_', '', str)
    str = re.sub('_$', '', str)
    str = re.sub('_+', '_', str)
    return str


# Check directory
with open("builder/src/font_awesome.json", "r") as font_awesome_file:
    font_awesome = json.loads(font_awesome_file.read())


def generate_font_awesome(name):
    if not name in font_awesome:
        return ""
    return '<i class="fa">%s</i>' % chr(int(font_awesome[name], 16))


def replace_font_awesome(matches):
    return generate_font_awesome(matches[1])


def custom_commands(html):
    html = html.replace("\\!", "\a")
    replacements = [
        ("!pagebreak", "<pagebreak>"),
        ("!icon:([\w-]+)", replace_font_awesome),
        ("<blockquote>\n<p>:(info|success|warning|danger)",
         "<blockquote class=\"\\1\">\n<p>"),
    ]
    for rep in replacements:
        html = re.sub(rep[0], rep[1], html)
    html = html.replace("\a", "!")
    return html


script_path = os.path.dirname(os.path.realpath(__file__))

# Cover
print("Generating cover...")
registerFont(TTFont('Roboto', 'builder/src/Roboto.ttf'))
registerFont(TTFont('FiraSans-Regular', 'builder/src/FiraSans-Regular.ttf'))
width = stringWidth(project_title, "Roboto", 50)
lines = [project_title]
if width > 370 and ' ' in project_title:
    lines = project_title.split(' ')

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFillColor(HexColor('#4C5270'))
can.setFont("Roboto", 50)

for i, text in enumerate(lines[::-1]):
    width = stringWidth(text, "Roboto", 50)
    can.drawString(535 - width, 390 + i * 55, text)

text = "© Coding Club " + project_campus.capitalize()
can.setFillColor(HexColor('#4B526F'))
can.setFont("FiraSans-Regular", 10)
width = stringWidth(text, "FiraSans-Regular", 10)
can.drawString(23, 32, text)

text = "VERSION " + project_version
can.setFillColor(HexColor('#8288A8'))
can.setFont("Roboto", 17)
width = stringWidth(text, "Roboto", 17)
can.drawString(535 - width, 335, text)
can.save()
packet.seek(0)

new_pdf = PdfReader(packet)
existing_pdf = PdfReader(open("builder/src/cover.pdf", "rb"))
output = PdfWriter()
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
outputStream = open("builder/cover.pdf", "wb")
output.write(outputStream)
outputStream.close()

# Headless browser

options = Options()
options.add_argument("-headless")
driver = webdriver.Firefox(options=options)

# Base HTML Template
print("Templating HTML...")
base_html = ""
with open("builder/base.html", "r") as base_html_file:
    base_html = base_html_file.read()

# Markdown parsing
print("Parsing MarkDown...")
with open(compile_file, "r") as md_file:
    markdown_content = md_file.read()
html_file_name = "builder/output.html"
output = markdown.markdown(markdown_content, extensions=[
                           'markdown.extensions.meta', 'markdown.extensions.codehilite', 'markdown.extensions.extra'])
base_html = base_html.replace("{{content}}", custom_commands(output))
with open(html_file_name, "w") as html_file:
    html_file.write(base_html)

# copy all files and directories in the current directory to builder
files = []
print("Copying files...")
for file in os.listdir(export_dir):
    if file not in ["builder", "cc_subjects.py", "src"] and not any([file.endswith(".%s" % ext) for ext in ["md", "pdf", "log", "txt"]]):
        files.append(file)
        os.system("cp -r %s/%s builder/" % (export_dir, file))

# Interpret JS code
print("Interpreting HTML...")
driver.get("file:///%s/%s" % (os.getcwd(), html_file_name))
sleep(2)
elem = driver.find_element(By.XPATH, "//*")
interpreted_html = elem.get_attribute("outerHTML")

with open(html_file_name, "w") as html_out_file:
    html_out_file.write(interpreted_html)

# Create final PDF file
print("Exporting PDF...")
pdf = HTML(html_file_name).write_pdf()
f = open("builder/output.pdf", 'wb')
f.write(pdf)
f.close()
# Merge 2 pdfs cover and output (output has multiple pages)
print("Merging PDFs...")
merger = PdfMerger()
merger.append(PdfReader(open("builder/cover.pdf", 'rb')))
merger.append(PdfReader(open("builder/output.pdf", 'rb')))
merger.write(export_dir + "/../" + str_to_snake_case(project_title) + ".pdf")

print("Removing temporary files...")
os.remove("builder/output.html")
os.remove("builder/output.pdf")
os.remove("builder/cover.pdf")
for file in files:
    os.system("rm -r builder/%s" % file)
print("Done.")


driver.quit()
