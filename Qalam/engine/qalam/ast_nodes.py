"""
Qalam AST Nodes - Abstract Syntax Tree representation
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union


@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    line: int = 0
    column: int = 0


@dataclass
class Document(ASTNode):
    """Root node representing the entire document"""
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List[ASTNode] = field(default_factory=list)
    doc_type: str = "memoir"
    language: str = "ar"


@dataclass
class Metadata(ASTNode):
    """Document metadata block"""
    properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class Chapter(ASTNode):
    """Chapter/Fasal node"""
    number: int = 0
    title: str = ""
    children: List[ASTNode] = field(default_factory=list)


@dataclass
class Section(ASTNode):
    """Section/Qism node"""
    title: str = ""
    children: List[ASTNode] = field(default_factory=list)


@dataclass
class Subsection(ASTNode):
    """Subsection/Far' node"""
    title: str = ""
    children: List[ASTNode] = field(default_factory=list)


@dataclass
class Environment(ASTNode):
    """Generic environment block ({{ ... }})"""
    env_type: str = ""  # abstract, introduction, quote, etc.
    reference: Optional[str] = None
    content: Union[str, List[ASTNode]] = ""
    properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class Paragraph(ASTNode):
    """Paragraph of text"""
    content: str = ""
    inline_formatting: List[tuple] = field(default_factory=list)  # [(type, text), ...]


@dataclass
class TextNode(ASTNode):
    """Plain text with optional formatting"""
    text: str = ""
    bold: bool = False
    italic: bool = False
    underline: bool = False


@dataclass
class Table(ASTNode):
    """Table environment"""
    caption: str = ""
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)


@dataclass
class Figure(ASTNode):
    """Figure/Image environment"""
    path: str = ""
    caption: str = ""
    width: str = "80%"
    properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class Equation(ASTNode):
    """Mathematical equation"""
    content: str = ""
    caption: str = ""
    label: Optional[str] = None


@dataclass
class List(ASTNode):
    """List (ordered or unordered)"""
    ordered: bool = False
    items: List[str] = field(default_factory=list)


@dataclass
class Quote(ASTNode):
    """Quotation block"""
    content: str = ""
    source: str = ""


@dataclass
class Definition(ASTNode):
    """Definition block"""
    term: str = ""
    definition: str = ""


@dataclass
class Note(ASTNode):
    """Note/Remark block"""
    content: str = ""
    note_type: str = "info"  # info, warning, important


@dataclass
class Citation(ASTNode):
    """Inline citation [ref: xxx]"""
    ref_id: str = ""


@dataclass
class PageBreak(ASTNode):
    """Manual page break <<<"""
    pass


@dataclass
class ReferenceEntry(ASTNode):
    """Bibliography entry (book, article, etc.)"""
    entry_type: str = ""  # book, article, thesis
    ref_id: str = ""
    fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class Comment(ASTNode):
    """Comment node (not rendered)"""
    content: str = ""


# Type alias for content that can be in environments
ContentNode = Union[str, Paragraph, TextNode, Table, Figure, Equation, List, Quote]
