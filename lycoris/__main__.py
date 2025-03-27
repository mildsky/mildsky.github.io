import os, time, sys, re
from dataclasses import dataclass
import typer
from lxml import etree

'''
code excution flow
1. find all markdown files in the input directory
2. for each markdown file, parse the markdown file
3. generate graph representation of the markdown files
4. using the graph, generate html files
5. write the html files to the output directory
6. done
'''

class Lycoris:
    '''
    Graph representation of markdown files
    It holds the relationships between markdown files
    It also holds the relationships between markdown files and their corresponding html files
    So, using this graph, we can easily remap the hyperlinks in the markdown files to the corresponding html files
    graph is n by n array where n is the number of nodes.
    if graph[i][j] == 1, then there is a link from node i to node j
    '''
    categories = []
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
    def pprint(self, element, **kwargs):
        xml = etree.tostring(element, pretty_print=True, **kwargs)
        print(xml.decode())
    def find_markdown_files(self, search_dir):
        """ Recursively find all markdown files in a directory """
        md_files = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith(".md"):
                    md_files.append(os.path.join(root, file))
        return md_files
    def find_html_files(self, search_dir):
        """ Recursively find all html files in a directory """
        html_files = []
        for root, _, files in os.walk(search_dir):
            for file in files:
                if file.endswith(".html"):
                    html_files.append(os.path.join(root, file))
        return html_files
    def preprocess(self):
        pass
    def parseMarkdown(self, filepath):
        root = etree.Element('mdtree')
        metadata = etree.SubElement(root, 'metadata')
        '''
        metadata:
        - filename
        - last modified date
        - created date
        - category
        - tags
        - 
        '''
        metadata.set('dirname', os.path.relpath(os.path.dirname(filepath), self.input_dir)) # assume input_dir is the root
        metadata.set('filename', os.path.basename(filepath))
        content = etree.SubElement(root, 'content')
        context = None
        with open(filepath, 'r', encoding='utf-8') as src:
            for line in src:
                line = line.rstrip()
                if re.match(r'^!category', line):
                    category = line.split(' ')[1].strip()
                    metadata.set('category', category)
                    self.categories.append(category)
                elif re.match(r'^!tags', line):
                    tags = etree.SubElement(metadata, 'tags')
                    for tag in line.split(' ')[1:]:
                        etree.SubElement(tags, 'tag').text = tag
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
                # elif line.startswith('#'):
                #     # add heading
                #     print(line)
                # elif line.startswith('##'):
                #     print(line)
                # elif line.startswith('###'):
                #     print(line)
                # elif line.startswith('####'):
                #     print(line)
                # elif line.startswith('#####'):
                #     print(line)
                # elif line.startswith('######'):
                #     print(line)
                # elif line.startswith('```') and context is None:
                #     # start code block
                #     print(line)
                # elif line.startswith('```') and context is not None:
                #     # end code block
                #     print(line)
                # elif line.startswith('*'):
                #     # list
                #     print(line)
                # elif line.startswith('1.'):
                #     # ordered list
                #     print(line)
                # else:
                #     print(line)
        return root
    def interprocess(self, etree):
        # add top bar
        # add side bar
        # add footer
        # add timeline
        # add search engine
        # add graph
        pass
    def buildHTML(self, mdtree, dry_run=False):
        html = etree.Element('html')
        head = etree.Element('head')
        body = etree.Element('body')
        html.append(head)
        html.append(body)
        styles = []
        scripts = []
        head_elements = []
        body_elements = []
        filename = mdtree.find('metadata').get('filename').replace('.md', '')
        dirname = mdtree.find('metadata').get('dirname')
        for style in styles:
            style_element = etree.Element('style')
            style_element.text = style
            head.append(style_element)
        for element in head_elements:
            head.append(element)
        for script in scripts:
            script_element = etree.Element('script')
            script_element.text = script
            body.append(script_element)
        for element in body_elements:
            body.append(element)
        if dry_run:
            # print(f"<!DOCTYPE html>\n{etree.tostring(self.html, pretty_print=True).decode()}")
            return etree.tostring(html, doctype="<!DOCTYPE html>", pretty_print=True).decode()
        else:
            output_file = f"{self.output_dir}/{dirname}/{filename}.html"
            dirname = f"{self.output_dir}/{dirname}"
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            print(f"Writing to {output_file}")
            html_string = etree.tostring(html, doctype="<!DOCTYPE html>", pretty_print=True).decode()
            with open(output_file, 'x', encoding='utf-8') as out:
                out.write(html_string)
            return html_string
    def postprocess(self):
        pass
    def clean(self, clean_dir, sure=False):
        if not sure:
            print("below files will be deleted")
            for root, _, files in os.walk(clean_dir):
                for file in files:
                    print(f"- {os.path.join(root, file)}")
            if input(f"Are you sure you want to delete all files in {clean_dir}?[yes/no]").lower() == 'yes':
                sure = True
            else:
                print("Aborted.")
                return False
        if sure:
            for root, _, files in os.walk(clean_dir):
                for file in files:
                    print(f"Deleting {os.path.join(root, file)}")
                    os.remove(os.path.join(root, file))
                    time.sleep(0.1)
            print("Cleaning done.")
        return True
    def navibar(self, tree):
        return tree
    def sidebar(self, tree):
        return tree
    def timeline(self, tree):
        return tree

app = typer.Typer()

@app.command()
def build(input_dir: str, output_dir: str):
    lyco = Lycoris(input_dir, output_dir)
    lyco.clean(output_dir, sure=True)
    print(f"Building {input_dir} to {output_dir}")
    md_files = lyco.find_markdown_files(input_dir)
    html_files = lyco.find_html_files(input_dir)
    print(f"found {len(md_files)} markdown files")
    for md in md_files:
        print(f"- {md}")
    for md_file in md_files:
        mdtree = lyco.parseMarkdown(md_file)
        lyco.pprint(mdtree)
        lyco.buildHTML(mdtree)

@app.command()
def clean(clean_dir: str, sure: bool = False):
    lyco = Lycoris()
    lyco.clean(clean_dir, sure)

app()