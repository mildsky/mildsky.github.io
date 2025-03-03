import os, time, sys
import glob
import typer
from lxml import etree

def pprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode())

class HTMLBuilder:
    def __init__(self):
        self.html = etree.Element('html')
        self.head = etree.Element('head')
        self.body = etree.Element('body')
        self.html.append(self.head)
        self.html.append(self.body)
        self.title = None
        self.styles = []
        self.scripts = []
        self.body_elements = []
        self.head_elements = []
        self.body.append(etree.Element('div'))
        self.body_div = self.body[0]
        self.body_div.attrib['class'] = 'container'
        self.body_div.attrib['id'] = 'main'
    def insertEtree(self, where, etree):
        if where == 'head':
            self.head.append(etree)
        elif where == 'body':
            self.body_div.append(etree)
    def toString(self):
        return etree.tostring(self.html, pretty_print=True).decode()


def find_markdown_files(directory):
    """
    Recursively finds all markdown files (.md) in the given directory.
    
    :param directory: The root directory to start searching from.
    :return: A list of markdown file paths with '/' as the separator.
    """
    files = glob.glob(os.path.join(directory, '**', '*.md'), recursive=True)
    return files

def find_html_files(directory):
    """
    Recursively finds all HTML files (.html) in the given directory.
    
    :param directory: The root directory to start searching from.
    :return: A list of HTML file paths.
    """
    files = glob.glob(os.path.join(directory, '**', '*.html'), recursive=True)
    return files

app = typer.Typer()

@app.command()
def build(input_dir: str, output_dir: str):
    print(f"Building {input_dir} to {output_dir}")
    md_files = find_markdown_files(input_dir)
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as src:
            print(src.read())
    html_files = find_html_files(input_dir)
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as src:
            print(src.read())
    builder = HTMLBuilder()
    pprint(builder.html)

app()