"""
Qalam Parser - Builds AST from tokens
"""

from typing import List, Optional, Dict, Any
from .lexer import Token, TokenType, lex
from .ast_nodes import (
    Document, Metadata, Chapter, Section, Subsection,
    Environment, Paragraph, TextNode, Table, Figure,
    Equation, List as QList, Quote, Definition, Note,
    Citation, PageBreak, ReferenceEntry, Comment, ASTNode
)
from .keywords import normalize_env, normalize_section, normalize_metadata


class ParseError(Exception):
    """Parser error exception"""
    pass


class QalamParser:
    """
    Parser for Qalam language
    Converts tokens into Abstract Syntax Tree (AST)
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type != TokenType.COMMENT]
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def error(self, message: str):
        """Raise a parse error"""
        token = self.current()
        raise ParseError(f"Parse error at line {token.line}: {message}")
    
    def current(self) -> Optional[Token]:
        """Get current token"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        """Look ahead at token"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Optional[Token]:
        """Move to next token and return current"""
        token = self.current()
        if self.pos < len(self.tokens):
            self.pos += 1
            self.current_token = self.current()
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect specific token type"""
        token = self.current()
        if not token or token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name if token else 'EOF'}")
        return self.advance()
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        token = self.current()
        return token and token.type in token_types
    
    def skip_newlines(self):
        """Skip newline tokens"""
        while self.match(TokenType.NEWLINE):
            self.advance()
    
    def parse(self) -> Document:
        """Parse tokens into AST Document"""
        document = Document()
        self.skip_newlines()
        
        # Parse metadata block
        if self.match(TokenType.DOC_START):
            document.metadata = self.parse_metadata()
        
        # Parse document body
        while not self.match(TokenType.EOF):
            self.skip_newlines()
            if self.match(TokenType.EOF):
                break
            
            node = self.parse_body_element()
            if node:
                document.children.append(node)
        
        return document
    
    def parse_metadata(self) -> Dict[str, Any]:
        """Parse @@ metadata block"""
        self.expect(TokenType.DOC_START)
        metadata = {}
        
        # Get document type
        self.skip_newlines()
        if self.match(TokenType.TEXT):
            doc_type = self.advance().value.strip()
            metadata['doc_type'] = doc_type
        
        # Parse properties
        while not self.match(TokenType.DOC_START) and not self.match(TokenType.EOF):
            self.skip_newlines()
            if self.match(TokenType.DOC_START):
                break
            
            if self.match(TokenType.TEXT):
                key_token = self.advance()
                key = normalize_metadata(key_token.value)
                
                if self.match(TokenType.ARROW):
                    self.advance()  # consume >>
                    
                    if self.match(TokenType.STRING):
                        value = self.advance().value
                        metadata[key] = value
                    elif self.match(TokenType.TEXT):
                        value = self.advance().value
                        metadata[key] = value
            
            elif self.match(TokenType.DOC_START):
                break
            else:
                self.advance()
        
        # End of metadata block
        if self.match(TokenType.DOC_START):
            self.advance()
        
        self.skip_newlines()
        return metadata
    
    def parse_body_element(self) -> Optional[ASTNode]:
        """Parse a body element (chapter, section, environment, etc.)"""
        token = self.current()
        
        if not token:
            return None
        
        # Chapter ===
        if token.type == TokenType.CHAPTER:
            return self.parse_chapter()
        
        # Section ---
        if token.type == TokenType.SECTION:
            return self.parse_section()
        
        # Subsection ~~~
        if token.type == TokenType.SUBSECTION:
            return self.parse_subsection()
        
        # Environment {{
        if token.type == TokenType.ENV_START:
            return self.parse_environment()
        
        # Page break <<<
        if token.type == TokenType.PAGE_BREAK:
            self.advance()
            return PageBreak(line=token.line)
        
        # Plain text paragraph
        return self.parse_paragraph()
    
    def parse_chapter(self) -> Chapter:
        """Parse chapter === ... ==="""
        token = self.expect(TokenType.CHAPTER)
        chapter = Chapter(line=token.line)
        
        # Extract number and title
        content = token.value
        parts = content.split(':', 1)
        
        # Try to extract chapter number
        first_part = parts[0].strip()
        words = first_part.split()
        for i, word in enumerate(words):
            if word.isdigit():
                chapter.number = int(word)
                break
        
        # Get title
        if len(parts) > 1:
            chapter.title = parts[1].strip()
        else:
            chapter.title = first_part
        
        # Parse chapter children
        chapter.children = []
        while not self.match(TokenType.EOF, TokenType.CHAPTER):
            self.skip_newlines()
            if self.match(TokenType.EOF, TokenType.CHAPTER):
                break
            
            child = self.parse_body_element()
            if child and not isinstance(child, Chapter):
                chapter.children.append(child)
            elif isinstance(child, Chapter):
                # Put back for parent to handle
                self.pos -= 1
                self.current_token = self.current()
                break
        
        return chapter
    
    def parse_section(self) -> Section:
        """Parse section --- ... ---"""
        token = self.expect(TokenType.SECTION)
        section = Section(line=token.line)
        
        # Extract title
        content = token.value
        if ':' in content:
            _, title = content.split(':', 1)
            section.title = title.strip()
        else:
            section.title = content.strip()
        
        # Parse section children
        section.children = []
        while not self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION):
            self.skip_newlines()
            if self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION):
                break
            
            child = self.parse_body_element()
            if child and not isinstance(child, (Chapter, Section)):
                section.children.append(child)
            elif isinstance(child, (Chapter, Section)):
                self.pos -= 1
                self.current_token = self.current()
                break
        
        return section
    
    def parse_subsection(self) -> Subsection:
        """Parse subsection ~~~ ... ~~~"""
        token = self.expect(TokenType.SUBSECTION)
        subsection = Subsection(line=token.line)
        
        # Extract title
        content = token.value
        if ':' in content:
            _, title = content.split(':', 1)
            subsection.title = title.strip()
        else:
            subsection.title = content.strip()
        
        # Parse subsection children (text and inline environments only)
        subsection.children = []
        while not self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION, TokenType.SUBSECTION):
            self.skip_newlines()
            if self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION, TokenType.SUBSECTION):
                break
            
            if self.match(TokenType.ENV_START):
                child = self.parse_environment()
                subsection.children.append(child)
            else:
                # Plain text
                text = self.parse_text_content()
                if text.strip():
                    subsection.children.append(TextNode(text=text.strip(), line=token.line))
        
        return subsection
    
    def parse_environment(self) -> Environment:
        """Parse {{ environment }} block"""
        start_token = self.expect(TokenType.ENV_START)
        env = Environment(line=start_token.line)
        
        # Get environment type
        self.skip_newlines()
        if self.match(TokenType.TEXT):
            type_token = self.advance()
            env.env_type = normalize_env(type_token.value)
            
            # Check for reference: {{ اقتباس >> المرجع }}
            if self.match(TokenType.ARROW):
                self.advance()
                if self.match(TokenType.STRING):
                    env.reference = self.advance().value
                elif self.match(TokenType.TEXT):
                    env.reference = self.advance().value
        
        self.skip_newlines()
        
        # Parse environment content
        content_parts = []
        properties = {}
        
        while not self.match(TokenType.ENV_END) and not self.match(TokenType.EOF):
            # Check for property: key >> "value"
            if self.match(TokenType.TEXT):
                key_token = self.peek()
                if self.peek(1) and self.peek(1).type == TokenType.ARROW:
                    self.advance()  # consume key
                    self.advance()  # consume >>
                    if self.match(TokenType.STRING):
                        value = self.advance().value
                        properties[key_token.value] = value
                        continue
                    elif self.match(TokenType.TEXT):
                        value = self.advance().value
                        properties[key_token.value] = value
                        continue
            
            # Check for table row
            if self.match(TokenType.TABLE_ROW):
                content_parts.append(self.advance())
                continue
            
            # Check for list item
            if self.match(TokenType.LIST_ITEM):
                content_parts.append(self.advance())
                continue
            
            # Check for nested environment
            if self.match(TokenType.ENV_START):
                # This might be end marker {{ /xxx }}
                if self.peek(1) and self.peek(1).type == TokenType.TEXT and self.peek(1).value.startswith('/'):
                    # End marker - should be handled by ENV_END
                    break
                content_parts.append(self.parse_environment())
                continue
            
            # Plain text content
            if not self.match(TokenType.ENV_END):
                text = self.parse_text_content()
                if text.strip():
                    content_parts.append(text)
            
            self.skip_newlines()
        
        # Consume closing }}
        if self.match(TokenType.ENV_END):
            self.advance()
        
        # Process content based on environment type
        if env.env_type in ['table']:
            env.content = self.parse_table_content(content_parts)
        elif env.env_type in ['list', 'قائمة']:
            env.content = self.parse_list_content(content_parts)
        elif env.env_type in ['figure', 'شكل']:
            env.content = self.parse_figure_content(properties)
        elif env.env_type in ['equation', 'معادلة']:
            env.content = self.parse_equation_content(content_parts, properties)
        else:
            env.content = '\n'.join(str(p) for p in content_parts if p).strip()
        
        env.properties = properties
        return env
    
    def parse_table_content(self, tokens: List) -> Table:
        """Parse table content from tokens"""
        table = Table()
        rows = []
        
        for token in tokens:
            if hasattr(token, 'type') and token.type == TokenType.TABLE_ROW:
                cells = [c.strip() for c in token.value.split('|')[1:-1]]
                if cells:
                    rows.append(cells)
        
        if rows:
            table.headers = rows[0]
            table.rows = rows[1:] if len(rows) > 1 else []
        
        return table
    
    def parse_list_content(self, tokens: List) -> QList:
        """Parse list content from tokens"""
        qlist = QList()
        
        for token in tokens:
            if hasattr(token, 'type'):
                if token.type == TokenType.LIST_ITEM:
                    qlist.items.append(token.value)
                elif token.type == TokenType.ORDERED_ITEM:
                    qlist.ordered = True
                    qlist.items.append(token.value)
            elif isinstance(token, str) and token.strip().startswith('-'):
                qlist.items.append(token.strip()[1:].strip())
        
        return qlist
    
    def parse_figure_content(self, properties: Dict) -> Figure:
        """Parse figure environment"""
        figure = Figure()
        figure.path = properties.get('path', '')
        figure.caption = properties.get('تعليق', properties.get('caption', ''))
        figure.width = properties.get('حجم', properties.get('width', '80%'))
        figure.properties = properties
        return figure
    
    def parse_equation_content(self, tokens: List, properties: Dict) -> Equation:
        """Parse equation environment"""
        eq = Equation()
        content_lines = [str(t) for t in tokens if isinstance(t, str)]
        eq.content = '\n'.join(content_lines).strip()
        eq.caption = properties.get('تعليق', properties.get('caption', ''))
        return eq
    
    def parse_paragraph(self) -> Optional[Paragraph]:
        """Parse a paragraph of text"""
        lines = []
        
        while not self.match(
            TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION,
            TokenType.SUBSECTION, TokenType.ENV_START, TokenType.PAGE_BREAK
        ):
            token = self.current()
            if not token:
                break
            
            if token.type == TokenType.NEWLINE:
                # Check if double newline (paragraph break)
                if self.peek(1) and self.peek(1).type == TokenType.NEWLINE:
                    self.advance()
                    break
                lines.append(' ')
                self.advance()
            elif token.type in [TokenType.TEXT, TokenType.STRING, TokenType.NUMBER]:
                lines.append(self.advance().value)
            elif token.type == TokenType.BOLD:
                lines.append(f"**{self.advance().value}**")
            elif token.type == TokenType.ITALIC:
                lines.append(f"*{self.advance().value}*")
            elif token.type == TokenType.UNDERLINE:
                lines.append(f"__{self.advance().value}__")
            elif token.type == TokenType.CITATION:
                lines.append(f"[ref: {self.advance().value}]")
            else:
                self.advance()
        
        content = ''.join(lines).strip()
        if content:
            return Paragraph(content=content)
        return None
    
    def parse_text_content(self) -> str:
        """Parse raw text content"""
        lines = []
        
        while not self.match(
            TokenType.EOF, TokenType.ENV_END, TokenType.ENV_START,
            TokenType.CHAPTER, TokenType.SECTION, TokenType.SUBSECTION
        ):
            token = self.current()
            if not token:
                break
            
            if token.type == TokenType.NEWLINE:
                lines.append('\n')
                self.advance()
            elif token.type in [TokenType.TEXT, TokenType.STRING, TokenType.NUMBER]:
                lines.append(self.advance().value)
            elif token.type == TokenType.TABLE_ROW:
                lines.append(self.advance().value)
            elif token.type == TokenType.LIST_ITEM:
                lines.append(f"- {self.advance().value}")
            else:
                self.advance()
        
        return ''.join(lines)


def parse(tokens: List[Token]) -> Document:
    """Convenience function to parse tokens into AST"""
    parser = QalamParser(tokens)
    return parser.parse()


def parse_source(source: str) -> Document:
    """Parse source code directly into AST"""
    tokens = lex(source)
    return parse(tokens)
