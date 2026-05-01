"""
Lexer for Qalam Language
المحلل المعجمي للغة قلم
"""

import re
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Token types for Qalam language"""
    # Structural
    DOC_START = auto()      # @@
    DOC_END = auto()        # @@
    ENV_START = auto()      # {{
    ENV_END = auto()        # }}
    ENV_CLOSE = auto()      # {{ /نوع
    
    # Section markers
    CHAPTER = auto()        # ===
    SECTION = auto()        # ---
    SUBSECTION = auto()     # ~~~
    
    # Property separator
    ARROW = auto()          # >>
    
    # Content
    STRING = auto()         # "text"
    NUMBER = auto()         # 123
    TEXT = auto()           # Regular text
    IDENTIFIER = auto()     # Keywords/identifiers
    
    # Formatting
    BOLD = auto()           # **text**
    ITALIC = auto()         # *text*
    UNDERLINE = auto()      # __text__
    CITATION = auto()       # [ref: id]
    
    # Special
    COMMENT = auto()        # # comment
    PAGE_BREAK = auto()     # <<<
    TABLE_ROW = auto()      # | cell |
    LIST_ITEM = auto()      # - item
    ORDERED_ITEM = auto()   # 1. item
    NEWLINE = auto()
    
    # End of file
    EOF = auto()


@dataclass
class Token:
    """Token class"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


class LexerError(Exception):
    """Lexer error with position information"""
    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Line {line}, Col {column}: {message}")


class Lexer:
    """
    Lexer for Qalam language
    Converts source text into tokens
    """
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def error(self, message: str):
        """Raise a lexer error"""
        raise LexerError(message, self.line, self.column)
    
    def peek(self, offset: int = 0) -> str:
        """Look at character at current position + offset"""
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def advance(self) -> str:
        """Advance position and return current character"""
        char = self.peek()
        self.pos += 1
        self.column += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace but preserve newlines"""
        while self.peek() in ' \t\r':
            self.advance()
    
    def read_string(self) -> str:
        """Read a quoted string"""
        quote = self.advance()  # consume opening quote
        result = ""
        
        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\\':
                self.advance()
                escape_char = self.advance()
                if escape_char == 'n':
                    result += '\n'
                elif escape_char == 't':
                    result += '\t'
                elif escape_char == quote:
                    result += quote
                else:
                    result += escape_char
            else:
                result += self.advance()
        
        if self.peek() == '\0':
            self.error("Unterminated string")
        
        self.advance()  # consume closing quote
        return result
    
    def read_identifier_or_keyword(self) -> str:
        """Read an identifier or keyword (Arabic, English, or French)"""
        result = ""
        
        # Arabic letters
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]')
        # Latin letters and numbers
        latin_pattern = re.compile(r'[a-zA-Z0-9_]')
        
        while True:
            char = self.peek()
            if arabic_pattern.match(char) or latin_pattern.match(char) or char in ' -:':
                result += self.advance()
            else:
                break
        
        return result.strip()
    
    def read_number(self) -> str:
        """Read a number"""
        result = ""
        while self.peek().isdigit():
            result += self.advance()
        return result
    
    def read_line_comment(self) -> str:
        """Read a line comment"""
        self.advance()  # consume #
        result = ""
        while self.peek() != '\n' and self.peek() != '\0':
            result += self.advance()
        return result
    
    def read_until_pattern(self, pattern: str) -> str:
        """Read text until a pattern is found"""
        result = ""
        pattern_len = len(pattern)
        
        while self.peek() != '\0':
            # Check if we've found the pattern
            if self.source[self.pos:self.pos + pattern_len] == pattern:
                break
            
            # Check for environment close pattern
            if pattern == '}}' and self.source[self.pos:self.pos + 4] == '{{ /':
                break
            
            result += self.advance()
        
        return result.rstrip()
    
    def tokenize(self) -> List[Token]:
        """Tokenize the entire source"""
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            char = self.peek()
            start_line = self.line
            start_col = self.column
            
            # Two-character tokens
            two_char = self.source[self.pos:self.pos + 2]
            
            # Check for @@ (document markers)
            if two_char == '@@':
                self.advance()
                self.advance()
                # Check if it's end marker (has space before content or newline)
                if self.tokens and self.tokens[-1].type != TokenType.DOC_START:
                    self.tokens.append(Token(TokenType.DOC_END, '@@', start_line, start_col))
                else:
                    self.tokens.append(Token(TokenType.DOC_START, '@@', start_line, start_col))
                continue
            
            # Check for {{ (environment start)
            if two_char == '{{':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ENV_START, '{{', start_line, start_col))
                continue
            
            # Check for }} (environment end)
            if two_char == '}}':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ENV_END, '}}', start_line, start_col))
                continue
            
            # Check for >> (arrow/property separator)
            if two_char == '>>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '>>', start_line, start_col))
                continue
            
            # Three-character tokens
            three_char = self.source[self.pos:self.pos + 3]
            
            # Check for === (chapter)
            if three_char == '===':
                for _ in range(3):
                    self.advance()
                self.tokens.append(Token(TokenType.CHAPTER, '===', start_line, start_col))
                continue
            
            # Check for --- (section)
            if three_char == '---':
                for _ in range(3):
                    self.advance()
                self.tokens.append(Token(TokenType.SECTION, '---', start_line, start_col))
                continue
            
            # Check for ~~~ (subsection)
            if three_char == '~~~':
                for _ in range(3):
                    self.advance()
                self.tokens.append(Token(TokenType.SUBSECTION, '~~~', start_line, start_col))
                continue
            
            # Check for <<< (page break)
            if three_char == '<<<':
                for _ in range(3):
                    self.advance()
                self.tokens.append(Token(TokenType.PAGE_BREAK, '<<<', start_line, start_col))
                continue
            
            # Single character tokens
            if char == '#':
                comment_text = self.read_line_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment_text, start_line, start_col))
                continue
            
            if char == '"' or char == "'":
                string_val = self.read_string()
                self.tokens.append(Token(TokenType.STRING, string_val, start_line, start_col))
                continue
            
            if char == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                continue
            
            if char == '|':
                # Table row
                self.advance()
                row_content = "|"
                while self.peek() != '\n' and self.peek() != '\0':
                    row_content += self.advance()
                self.tokens.append(Token(TokenType.TABLE_ROW, row_content, start_line, start_col))
                continue
            
            if char == '-':
                # Could be list item or part of section marker
                if self.peek(1) == ' ':
                    self.advance()  # consume -
                    self.advance()  # consume space
                    self.tokens.append(Token(TokenType.LIST_ITEM, '-', start_line, start_col))
                    continue
            
            # Number followed by dot (ordered list)
            if char.isdigit() and self.peek(1) == '.':
                num = self.read_number()
                if self.peek() == '.':
                    self.advance()  # consume .
                    self.advance()  # consume space after .
                    self.tokens.append(Token(TokenType.ORDERED_ITEM, num, start_line, start_col))
                    continue
            
            # Identifier or keyword (including Arabic text)
            if char.isalnum() or ord(char) > 0x0600:  # Arabic unicode range
                ident = self.read_identifier_or_keyword()
                if ident:
                    self.tokens.append(Token(TokenType.IDENTIFIER, ident, start_line, start_col))
                    continue
            
            # Regular text (until next token)
            if char not in ' \t\r\n':
                text = self.read_until_pattern('\n')
                if text.strip():
                    self.tokens.append(Token(TokenType.TEXT, text.strip(), start_line, start_col))
                continue
            
            # Skip unknown characters
            self.advance()
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def tokenize_to_text(self) -> str:
        """Tokenize and return human-readable representation"""
        tokens = self.tokenize()
        return '\n'.join(str(t) for t in tokens)
