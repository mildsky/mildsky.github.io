import os, time, sys
import typer
from lxml import etree, html
# from .plugin import *
import re   # regex
from dataclasses import dataclass

'''
code excution flow
1. find all markdown files in the input directory
2. for each markdown file, parse the markdown file
3. generate graph representation of the markdown files
4. using the graph, generate html files
5. write the html files to the output directory
6. done
'''

def pprint(element, **kwargs):
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    print(xml.decode())

def find_markdown_files(directory):
    """ Recursively find all markdown files in a directory """
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def find_html_files(directory):
    """ Recursively find all html files in a directory """
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

class MarkdownParser:
    def __init__(self, filepath, input_dir, output_dir):
        self.filepath = filepath
        self.root = etree.Element('root')
        self.metadata = etree.SubElement(self.root, 'metadata')
        self.metadata.set('filename', os.path.basename(filepath))
        self.metadata.set('dirname', os.path.relpath(os.path.dirname(filepath), input_dir))
        self.content = etree.SubElement(self.root, 'content')
        self.context = None
    def parseMarkdown(self):
        with open(self.filepath, 'r', encoding='utf-8') as src:
            for line in src:
                line = line.rstrip()  # Remove trailing whitespace
                
                # if line.startswith('```'):
                #     if self.context is None:
                #         self.context = 'code'
                #         code_block = etree.SubElement(self.content, 'code')
                #     else:
                #         self.context = None
                #     continue
                
                # if self.context == 'code':
                #     if code_block is not None:
                #         code_block.text = (code_block.text or '') + '\n' + line if code_block.text else line
                #     continue
                
                # if re.match(r'^#{1,6} ', line):
                #     level = line.count('#', 0, 6)
                #     heading = etree.SubElement(self.content, f'h{level}')
                #     heading.text = line[level+1:].strip()
                #     continue
                
                # if re.match(r'^\d+\. ', line):
                #     if current_list is None or current_list.tag != 'ordered_list':
                #         current_list = etree.SubElement(self.content, 'ordered_list')
                #     item = etree.SubElement(current_list, 'li')
                #     item.text = line.split('. ', 1)[1]
                #     continue
                
                # if line.startswith('* ') or line.startswith('- '):
                #     if current_list is None or current_list.tag != 'unordered_list':
                #         current_list = etree.SubElement(self.content, 'unordered_list')
                #     item = etree.SubElement(current_list, 'li')
                #     item.text = line[2:]
                #     continue
                
                # if line.strip() == '':
                #     current_list = None  # Reset list context
                #     continue
                
                # paragraph = etree.SubElement(self.content, 'p')
                # paragraph.text = line

                # check line by line for markdown syntax using regex
                if line.startswith('!'):
                    # do custom logic
                    print(line)
                elif line.startswith('#'):
                    # add heading
                    print(line)
                elif line.startswith('##'):
                    print(line)
                elif line.startswith('###'):
                    print(line)
                elif line.startswith('####'):
                    print(line)
                elif line.startswith('#####'):
                    print(line)
                elif line.startswith('######'):
                    print(line)
                elif line.startswith('```') and self.context is None:
                    # start code block
                    print(line)
                elif line.startswith('```') and self.context is not None:
                    # end code block
                    print(line)
                elif line.startswith('*'):
                    # list
                    print(line)
                elif line.startswith('1.'):
                    # ordered list
                    print(line)
                else:
                    print(line)
        return self.root

class Lycoris:
    '''
    Graph representation of markdown files
    It holds the relationships between markdown files
    It also holds the relationships between markdown files and their corresponding html files
    So, using this graph, we can easily remap the hyperlinks in the markdown files to the corresponding html files
    graph is n by n array where n is the number of nodes.
    if graph[i][j] == 1, then there is a link from node i to node j
    '''
    @dataclass
    class Node:
        markdown: str
        html: str
        links: list
    def __init__(self):
        self.node = self.Node(markdown=None, html=None, links=[])

class HTMLBuilder:
    def __init__(self):
        self.html = etree.Element('html')
        self.head = etree.Element('head')
        self.body = etree.Element('body')
        self.html.append(self.head)
        self.html.append(self.body)
        self.styles = []
        self.scripts = []
        self.head_elements = []
        self.body_elements = []
        self.filename = None
        self.relative_path = None
    def build(self, mdtree):
        for style in self.styles:
            style_element = etree.Element('style')
            style_element.text = style
            self.head.append(style_element)
        for element in self.head_elements:
            self.head.append(element)
        for script in self.scripts:
            script_element = etree.Element('script')
            script_element.text = script
            self.body.append(script_element)
        for element in self.body_elements:
            self.body.append(element)
    def fromMarkdown(self, input_dir, markdown: str):
        filename = markdown
        dirname = os.path.dirname(markdown)
        reldir = os.path.relpath(dirname, input_dir)
        self.filename = os.path.relpath(markdown, input_dir)
        # remove the .md extension
        self.filename = self.filename[:-3] # it is assuming makrdown files were found by find_markdown_files
        # with open(markdown, 'r', encoding='utf-8') as src:
        #     print(src.read())
    def toString(self):
        # return f"<!DOCTYPE html>\n{etree.tostring(self.html, pretty_print=True).decode()}"
        return etree.tostring(self.html, doctype="<!DOCTYPE html>", pretty_print=True).decode()
    def toHTML(self, output_dir: str):
        output_file = f"{output_dir}/{self.filename}.html"
        dirname = os.path.dirname(output_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        print(f"Writing to {output_file}")
        with open(output_file, 'x', encoding='utf-8') as out:
            out.write(self.toString())
        return self.toString()
    def clean(self, build_dir, sure=False):
        if not sure:
            print("below files will be deleted")
            for root, _, files in os.walk(build_dir):
                for file in files:
                    print(f"- {os.path.join(root, file)}")
            if input(f"Are you sure you want to delete all files in {build_dir}?[yes/no]").lower() == 'yes':
                sure = True
            else:
                print("Aborted.")
                return False
        if sure:
            for root, _, files in os.walk(build_dir):
                for file in files:
                    print(f"Deleting {os.path.join(root, file)}")
                    os.remove(os.path.join(root, file))
                    time.sleep(0.1)
            print("Cleaning done.")
        return True

app = typer.Typer()

@app.command()
def build(input_dir: str, output_dir: str):
    print(f"Building {input_dir} to {output_dir}")
    md_files = find_markdown_files(input_dir)
    print(f"found {len(md_files)} markdown files")
    for md in md_files:
        print(f"- {md}")
    builder = HTMLBuilder()
    builder.clean(build_dir=output_dir)
    for md_file in md_files:
        parser = MarkdownParser(md_file, input_dir, output_dir)
        pprint(parser.parseMarkdown())
        builder = HTMLBuilder()
        builder.fromMarkdown(input_dir, md_file)
        builder.toHTML(output_dir)
        # with open(md_file, 'r', encoding='utf-8') as src:
        #     print(src.read())
    # html_files = find_htm l_files(input_dir)
    # for html_file in html_files:
    #     with open(html_file, 'r', encoding='utf-8') as src:
    #         print(src.read())

@app.command()
def clean(build_dir: str, sure: bool = False):
    builder = HTMLBuilder()
    builder.clean(build_dir, sure)

app()