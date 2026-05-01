"""
Qalam Lexer - Tokenizes .qlm source code
"""

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Any


class TokenType(Enum):
    """Token types for Qalam language"""
    # Document structure
    DOC_START = auto()      # @@
    DOC_END = auto()        # @@
    CHAPTER = auto()        # === ... ===
    SECTION = auto()        # --- ... ---
    SUBSECTION = auto()     # ~~~ ... ~~~
    
    # Environments
    ENV_START = auto()      # {{
    ENV_END = auto()        # }}
    ENV_CLOSE = auto()      # {{ /... }}
    
    # Properties
    PROPERTY = auto()       # key >> "value"
    ARROW = auto()          # >>
    
    # Content
    TEXT = auto()           # Plain text
    STRING = auto()         # "string"
    NUMBER = auto()         # 123
    
    # Formatting
    BOLD = auto()           # **text**
    ITALIC = auto()         # *text*
    UNDERLINE = auto()      # __text__
    
    # Tables & Lists
    TABLE_ROW = auto()      # | cell | cell |
    LIST_ITEM = auto()      # - item
    ORDERED_ITEM = auto()   # 1. item
    
    # Special
    PAGE_BREAK = auto()     # <<<
    CITATION = auto()       # [ref: xxx]
    COMMENT = auto()        # # comment
    
    # Meta
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a lexical token"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line})"


class QalamLexer:
    """
    Lexer for Qalam language (.qlm files)
    Converts source text into tokens
    """
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def error(self, message: str):
        """Raise a lexical error"""
        raise SyntaxError(f"Lexer error at line {self.line}, col {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        """Look at character at current position + offset"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to next character and return current"""
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace but preserve newlines"""
        while self.peek() and self.peek().isspace() and self.peek() != '\n':
            self.advance()
    
    def read_line(self) -> str:
        """Read until end of line"""
        result = []
        while self.peek() and self.peek() != '\n':
            result.append(self.advance())
        return ''.join(result)
    
    def read_string(self) -> str:
        """Read a quoted string"""
        quote = self.advance()  # consume opening quote
        result = []
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                escaped = self.advance()
                if escaped:
                    result.append(escaped)
            else:
                result.append(self.advance())
        if self.peek() == quote:
            self.advance()  # consume closing quote
        return ''.join(result)
    
    def tokenize(self) -> List[Token]:
        """Convert source to list of tokens"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
                
            char = self.peek()
            start_line = self.line
            start_col = self.column
            
            # Comments
            if char == '#':
                self.advance()
                comment = self.read_line()
                self.tokens.append(Token(TokenType.COMMENT, comment, start_line, start_col))
                continue
            
            # Newline
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                continue
            
            # Page break
            if self.peek(0) == '<' and self.peek(1) == '<' and self.peek(2) == '<':
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.PAGE_BREAK, '<<<', start_line, start_col))
                continue
            
            # Document delimiters @@
            if char == '@' and self.peek(1) == '@':
                self.advance()
                self.advance()
                # Check if it's start or end based on context
                self.tokens.append(Token(TokenType.DOC_START, '@@', start_line, start_col))
                continue
            
            # Chapter ===
            if char == '=' and self.peek(1) == '=' and self.peek(2) == '=':
                self.advance()
                self.advance()
                self.advance()
                content = self.read_line().strip(' =')
                self.tokens.append(Token(TokenType.CHAPTER, content, start_line, start_col))
                continue
            
            # Section ---
            if char == '-' and self.peek(1) == '-' and self.peek(2) == '-':
                self.advance()
                self.advance()
                self.advance()
                content = self.read_line().strip(' -')
                self.tokens.append(Token(TokenType.SECTION, content, start_line, start_col))
                continue
            
            # Subsection ~~~
            if char == '~' and self.peek(1) == '~' and self.peek(2) == '~':
                self.advance()
                self.advance()
                self.advance()
                content = self.read_line().strip(' ~')
                self.tokens.append(Token(TokenType.SUBSECTION, content, start_line, start_col))
                continue
            
            # Environment start {{
            if char == '{' and self.peek(1) == '{':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ENV_START, '{{', start_line, start_col))
                continue
            
            # Environment close }}
            if char == '}' and self.peek(1) == '}':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ENV_END, '}}', start_line, start_col))
                continue
            
            # Property arrow >>
            if char == '>' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '>>', start_line, start_col))
                continue
            
            # Bold **text**
            if char == '*' and self.peek(1) == '*':
                self.advance()
                self.advance()
                bold_text = []
                while self.peek() and not (self.peek() == '*' and self.peek(1) == '*'):
                    bold_text.append(self.advance())
                if self.peek() == '*':
                    self.advance()
                    self.advance()
                self.tokens.append(Token(TokenType.BOLD, ''.join(bold_text), start_line, start_col))
                continue
            
            # Italic *text*
            if char == '*' and self.peek(1) != '*':
                self.advance()
                italic_text = []
                while self.peek() and self.peek() != '*':
                    italic_text.append(self.advance())
                if self.peek() == '*':
                    self.advance()
                self.tokens.append(Token(TokenType.ITALIC, ''.join(italic_text), start_line, start_col))
                continue
            
            # Underline __text__
            if char == '_' and self.peek(1) == '_':
                self.advance()
                self.advance()
                uline_text = []
                while self.peek() and not (self.peek() == '_' and self.peek(1) == '_'):
                    uline_text.append(self.advance())
                if self.peek() == '_':
                    self.advance()
                    self.advance()
                self.tokens.append(Token(TokenType.UNDERLINE, ''.join(uline_text), start_line, start_col))
                continue
            
            # Table row
            if char == '|':
                row_content = self.read_line()
                self.tokens.append(Token(TokenType.TABLE_ROW, row_content, start_line, start_col))
                continue
            
            # List item
            if char == '-' and (not self.peek(1) or self.peek(1).isspace()):
                self.advance()
                item_content = self.read_line().strip()
                self.tokens.append(Token(TokenType.LIST_ITEM, item_content, start_line, start_col))
                continue
            
            # Ordered list item
            if char.isdigit() and self.peek(1) == '.':
                num = ''
                while self.peek() and self.peek().isdigit():
                    num += self.advance()
                self.advance()  # consume .
                item_content = self.read_line().strip()
                self.tokens.append(Token(TokenType.ORDERED_ITEM, item_content, start_line, start_col))
                continue
            
            # Citation [ref: xxx]
            if char == '[':
                self.advance()
                cite_content = []
                while self.peek() and self.peek() != ']':
                    cite_content.append(self.advance())
                if self.peek() == ']':
                    self.advance()
                self.tokens.append(Token(TokenType.CITATION, ''.join(cite_content), start_line, start_col))
                continue
            
            # String
            if char in '"\'':
                string_val = self.read_string()
                self.tokens.append(Token(TokenType.STRING, string_val, start_line, start_col))
                continue
            
            # Number
            if char.isdigit():
                num = []
                while self.peek() and (self.peek().isdigit() or self.peek() in '.-'):
                    num.append(self.advance())
                self.tokens.append(Token(TokenType.NUMBER, ''.join(num), start_line, start_col))
                continue
            
            # Identifier / Keyword
            if char.isalpha() or char in 'أبتثجحخدذرزسشصضطظعغفقكلمنهويآإؤئ':
                ident = []
                while self.peek() and (self.peek().isalnum() or self.peek() in 'أبتثجحخدذرزسشصضطظعغفقكلمنهويآإؤئ_'):
                    ident.append(self.advance())
                self.tokens.append(Token(TokenType.TEXT, ''.join(ident), start_line, start_col))
                continue
            
            # Unknown character - skip or error
            self.advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens


def lex(source: str) -> List[Token]:
    """Convenience function to tokenize source"""
    lexer = QalamLexer(source)
    return lexer.tokenize()
