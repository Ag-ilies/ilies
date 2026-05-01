"""
Parser for Qalam Language
المحلل النحوي للغة قلم
"""

from typing import List, Optional, Dict, Any
from .lexer import Lexer, Token, TokenType, LexerError
from .ast_nodes import (
    Document, Metadata, Property, Chapter, Section, Subsection,
    Environment, Paragraph, TableNode, Figure, Equation, Quote,
    Definition, Note, QList, Reference, Bibliography,
    Comment, PageBreak, TextRun, ASTNode
)
from .keywords import Keywords


class ParserError(Exception):
    """Parser error with position information"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Line {line}, Col {column}: {message}")


class Parser:
    """
    Parser for Qalam language
    Converts tokens into AST
    """
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None
    
    def error(self, message: str):
        """Raise a parser error"""
        token = self.current()
        raise ParserError(message, token.line if token else 0, token.column if token else 0)
    
    def current(self) -> Optional[Token]:
        """Get current token"""
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        """Look ahead at token"""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return None
        return self.tokens[pos]
    
    def advance(self) -> Optional[Token]:
        """Advance to next token"""
        token = self.current()
        self.pos += 1
        self.current_token = self.current()
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        """Expect a specific token type"""
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
        """Parse the entire document"""
        document = Document()
        
        # Skip initial whitespace
        self.skip_newlines()
        
        # Parse metadata block if present
        if self.match(TokenType.DOC_START):
            document.metadata = self.parse_metadata()
        
        # Parse document body
        self.skip_newlines()
        while not self.match(TokenType.EOF):
            node = self.parse_body_element()
            if node:
                document.children.append(node)
            self.skip_newlines()
        
        return document
    
    def parse_metadata(self) -> Dict[str, Any]:
        """Parse metadata block (@@ ... @@)"""
        metadata = {}
        
        self.expect(TokenType.DOC_START)
        self.skip_newlines()
        
        # Parse document type
        if self.match(TokenType.IDENTIFIER):
            doc_type = self.advance().value.strip()
            if Keywords.is_document_type(doc_type):
                metadata['doc_type'] = Keywords.normalize_environment(doc_type)
        
        self.skip_newlines()
        
        # Parse properties
        while self.match(TokenType.IDENTIFIER):
            key_token = self.advance()
            
            # Skip if we hit end marker
            if key_token.value.strip() == '@@':
                break
            
            self.skip_newlines()
            
            # Expect >> arrow
            if not self.match(TokenType.ARROW):
                continue
            
            self.advance()  # consume >>
            self.skip_newlines()
            
            # Get value
            value = None
            if self.match(TokenType.STRING):
                value = self.advance().value
            elif self.match(TokenType.IDENTIFIER):
                value = self.advance().value
            
            if value:
                normalized_key = Keywords.normalize_metadata_key(key_token.value)
                metadata[normalized_key] = value
            
            self.skip_newlines()
        
        # Consume closing @@
        if self.match(TokenType.DOC_END):
            self.advance()
        
        return metadata
    
    def parse_body_element(self) -> Optional[ASTNode]:
        """Parse a body element (chapter, section, environment, etc.)"""
        self.skip_newlines()
        
        token = self.current()
        if not token:
            return None
        
        # Chapter (===)
        if token.type == TokenType.CHAPTER:
            return self.parse_chapter()
        
        # Section (---)
        if token.type == TokenType.SECTION:
            return self.parse_section()
        
        # Subsection (~~~)
        if token.type == TokenType.SUBSECTION:
            return self.parse_subsection()
        
        # Environment ({{ }})
        if token.type == TokenType.ENV_START:
            return self.parse_environment()
        
        # Page break (<<<)
        if token.type == TokenType.PAGE_BREAK:
            self.advance()
            return PageBreak(line=token.line, column=token.column)
        
        # Comment
        if token.type == TokenType.COMMENT:
            self.advance()
            return Comment(text=token.value, line=token.line, column=token.column)
        
        # Regular paragraph text
        return self.parse_paragraph()
    
    def parse_chapter(self) -> Chapter:
        """Parse chapter (=== فصل N: العنوان ===)"""
        token = self.expect(TokenType.CHAPTER)
        chapter = Chapter(line=token.line, column=token.column)
        
        # Collect title text until ===
        title_parts = []
        while not self.match(TokenType.CHAPTER, TokenType.EOF):
            t = self.advance()
            if t and t.value:
                title_parts.append(t.value)
        
        title = ' '.join(title_parts).strip()
        
        # Try to extract chapter number
        import re
        # Arabic: فصل 1 or فصل: 1
        match_ar = re.search(r'فصل\s*(\d+)', title)
        # English: Chapter 1
        match_en = re.search(r'[Cc]hapter\s*(\d+)', title)
        # French: Chapitre 1
        match_fr = re.search(r'[Cc]hapitre\s*(\d+)', title)
        
        if match_ar or match_en or match_fr:
            match = match_ar or match_en or match_fr
            chapter.number = int(match.group(1))
        
        chapter.title = title
        self.skip_newlines()
        
        # Parse chapter children
        while not self.match(TokenType.EOF, TokenType.CHAPTER):
            if self.match(TokenType.SECTION, TokenType.SUBSECTION, 
                         TokenType.ENV_START, TokenType.PAGE_BREAK):
                child = self.parse_body_element()
                if child:
                    chapter.children.append(child)
            elif self.match(TokenType.TEXT, TokenType.LIST_ITEM, TokenType.TABLE_ROW):
                # Inline content in chapter
                para = self.parse_paragraph()
                if para:
                    chapter.children.append(para)
            else:
                break
        
        return chapter
    
    def parse_section(self) -> Section:
        """Parse section (--- قسم: العنوان ---)"""
        token = self.expect(TokenType.SECTION)
        section = Section(line=token.line, column=token.column)
        
        # Collect title text until ---
        title_parts = []
        while not self.match(TokenType.SECTION, TokenType.EOF):
            t = self.advance()
            if t and t.value:
                title_parts.append(t.value)
        
        section.title = ' '.join(title_parts).strip()
        self.skip_newlines()
        
        # Parse section children
        while not self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION):
            if self.match(TokenType.SUBSECTION, TokenType.ENV_START, 
                         TokenType.PAGE_BREAK):
                child = self.parse_body_element()
                if child:
                    section.children.append(child)
            elif self.match(TokenType.TEXT, TokenType.LIST_ITEM, TokenType.TABLE_ROW):
                para = self.parse_paragraph()
                if para:
                    section.children.append(para)
            else:
                break
        
        return section
    
    def parse_subsection(self) -> Subsection:
        """Parse subsection (~~~ فرع: العنوان ~~~)"""
        token = self.expect(TokenType.SUBSECTION)
        subsection = Subsection(line=token.line, column=token.column)
        
        # Collect title text until ~~~
        title_parts = []
        while not self.match(TokenType.SUBSECTION, TokenType.EOF):
            t = self.advance()
            if t and t.value:
                title_parts.append(t.value)
        
        subsection.title = ' '.join(title_parts).strip()
        self.skip_newlines()
        
        # Parse subsection children
        while not self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION, 
                            TokenType.SUBSECTION):
            child = self.parse_body_element()
            if child:
                subsection.children.append(child)
            else:
                break
        
        return subsection
    
    def parse_environment(self) -> Environment:
        """Parse environment ({{ نوع }} ... {{ /نوع }})"""
        start_token = self.expect(TokenType.ENV_START)
        env = Environment(line=start_token.line, column=start_token.column)
        
        # Get environment type
        self.skip_newlines()
        if self.match(TokenType.IDENTIFIER):
            env_type = self.advance().value.strip()
            env.env_type = Keywords.normalize_environment(env_type)
        
        # Check for reference (>> "ref")
        self.skip_newlines()
        if self.match(TokenType.ARROW):
            self.advance()  # consume >>
            self.skip_newlines()
            if self.match(TokenType.STRING):
                env.reference = self.advance().value
        
        # Parse environment properties
        self.skip_newlines()
        while self.match(TokenType.IDENTIFIER):
            key_token = self.peek()
            
            # Check if it's the close marker
            next_token = self.peek(1)
            if next_token and next_token.type == TokenType.ARROW:
                self.advance()  # consume key
                self.advance()  # consume >>
                self.skip_newlines()
                
                value = None
                if self.match(TokenType.STRING):
                    value = self.advance().value
                elif self.match(TokenType.IDENTIFIER):
                    value = self.advance().value
                
                if value:
                    env.properties[key_token.value] = value
            else:
                break
            
            self.skip_newlines()
        
        # Consume closing }}
        if self.match(TokenType.ENV_END):
            self.advance()
        
        self.skip_newlines()
        
        # Parse environment content
        content_lines = []
        while not self.match(TokenType.EOF):
            # Check for closing tag {{ /type }}
            if self.match(TokenType.ENV_START):
                # Look ahead for /
                next_pos = self.pos + 1
                if next_pos < len(self.tokens):
                    next_tok = self.tokens[next_pos]
                    if next_tok and next_tok.type == TokenType.IDENTIFIER:
                        if next_tok.value.strip().startswith('/'):
                            # Found closing tag
                            self.advance()  # consume {{
                            self.advance()  # consume /type
                            self.skip_newlines()
                            if self.match(TokenType.ENV_END):
                                self.advance()  # consume }}
                            break
            
            # Collect content
            t = self.advance()
            if t:
                if t.type == TokenType.TEXT:
                    content_lines.append(t.value)
                elif t.type == TokenType.NEWLINE:
                    content_lines.append('\n')
                elif t.type == TokenType.BOLD:
                    content_lines.append(f'**{t.value}**')
                elif t.type == TokenType.ITALIC:
                    content_lines.append(f'*{t.value}*')
                elif t.type == TokenType.LIST_ITEM:
                    content_lines.append(f'- ')
                elif t.type == TokenType.TABLE_ROW:
                    content_lines.append(t.value)
        
        env.content = ''.join(content_lines).strip()
        
        return env
    
    def parse_paragraph(self) -> Optional[Paragraph]:
        """Parse regular paragraph text"""
        token = self.current()
        if not token:
            return None
        
        text_parts = []
        start_line = token.line
        start_col = token.column
        
        # Collect text until we hit a structural element
        while not self.match(TokenType.EOF, TokenType.CHAPTER, TokenType.SECTION,
                            TokenType.SUBSECTION, TokenType.ENV_START, 
                            TokenType.PAGE_BREAK):
            t = self.advance()
            if t:
                if t.type == TokenType.TEXT:
                    text_parts.append(t.value)
                elif t.type == TokenType.NEWLINE:
                    text_parts.append(' ')
                elif t.type == TokenType.LIST_ITEM:
                    # Start of list - stop paragraph
                    break
                elif t.type == TokenType.TABLE_ROW:
                    # Start of table - stop paragraph
                    break
                elif t.type == TokenType.COMMENT:
                    continue
        
        text = ' '.join(text_parts).strip()
        if text:
            return Paragraph(text=text, line=start_line, column=start_col)
        
        return None
