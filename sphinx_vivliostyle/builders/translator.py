from docutils import nodes
from sphinx.builders import Builder
from sphinx.writers.html import HTMLTranslator
from docutils.nodes import Element, Node,Text,document
from sphinx import addnodes
import re

class vivliostyleTransrator(HTMLTranslator):
    def __init__(self, document: document, builder: Builder) -> None:
        super().__init__(document, builder)
        self.section_level=-1

    def visit_section(self,node:Element):
        self.section_level+=1
    
    def depart_section(self,node:Element):
        self.section_level-=1
    
    def visit_title(self,node:Element):
        if self.section_level<=0:
            raise nodes.SkipNode
        
        self.body.append("\n\n"+self.section_level*"#" + " ")
    
    def depart_title(self,node:Element):
        self.body.append("\n\n")

    def visit_math(self, node: Element, math_env: str = '') -> None:
        self.body.append('$')
    
    def depart_math(self, node: Element, math_env: str = '') -> None:
        self.body.append('$')
    
    def visit_math_block(self, node: Element, math_env: str = '') -> None:
        self.body.append('\n$$\n')
    
    def depart_math_block(self, node: Element, math_env: str = '') -> None:
        self.body.append(re.sub('\n*$','',self.body.pop())+'\n')
        self.body.append('$$\n')
    
    def visit_paragraph(self,node:Element):
        self.body.append('\n')
    
    def depart_paragraph(self, node: Element) -> None:
        self.body.append('\n')

