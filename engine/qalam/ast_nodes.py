"""
AST Nodes for Qalam Language
عقد الشجرة النحوية للغة قلم
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ASTNode:
    """Base AST node class"""
    line: int = 0
    column: int = 0


@dataclass
class Document(ASTNode):
    """Root document node"""
    metadata: Dict[str, Any] = field(default_factory=dict)
    children: List['ASTNode'] = field(default_factory=list)
    doc_type: str = "memoir"


@dataclass
class Metadata(ASTNode):
    """Metadata block (@@ ... @@)"""
    properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class Property(ASTNode):
    """Property key-value pair (key >> "value")"""
    key: str = ""
    value: Any = None


@dataclass
class Chapter(ASTNode):
    """Chapter (=== فصل N: العنوان ===)"""
    number: Optional[int] = None
    title: str = ""
    children: List['ASTNode'] = field(default_factory=list)


@dataclass
class Section(ASTNode):
    """Section (--- قسم: العنوان ---)"""
    title: str = ""
    children: List['ASTNode'] = field(default_factory=list)


@dataclass
class Subsection(ASTNode):
    """Subsection (~~~ فرع: العنوان ~~~)"""
    title: str = ""
    children: List['ASTNode'] = field(default_factory=list)


@dataclass
class Environment(ASTNode):
    """Environment block ({{ نوع }} ... {{ /نوع }})"""
    env_type: str = ""
    reference: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    content: str = ""
    children: List['ASTNode'] = field(default_factory=list)


@dataclass
class Paragraph(ASTNode):
    """Regular paragraph text"""
    text: str = ""
    inline_formatting: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TableNode(ASTNode):
    """Table environment"""
    caption: str = ""
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)


@dataclass
class Figure(ASTNode):
    """Figure environment"""
    path: str = ""
    caption: str = ""
    scale: str = "100%"
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Equation(ASTNode):
    """Equation environment"""
    content: str = ""
    caption: str = ""


@dataclass
class Quote(ASTNode):
    """Quote environment"""
    content: str = ""
    reference: str = ""


@dataclass
class Definition(ASTNode):
    """Definition environment"""
    content: str = ""


@dataclass
class Note(ASTNode):
    """Note environment"""
    content: str = ""


@dataclass
class QList(ASTNode):
    """List environment"""
    ordered: bool = False
    items: List[str] = field(default_factory=list)


@dataclass
class Reference(ASTNode):
    """Reference entry (book, article, etc.)"""
    ref_type: str = ""
    ref_id: str = ""
    fields: Dict[str, str] = field(default_factory=dict)


@dataclass
class Bibliography(ASTNode):
    """Bibliography/References section"""
    entries: List[Reference] = field(default_factory=list)


@dataclass
class InlineFormat(ASTNode):
    """Inline formatting (bold, italic, underline)"""
    format_type: str = ""  # bold, italic, underline
    content: str = ""


@dataclass
class Citation(ASTNode):
    """Citation reference [ref: id]"""
    ref_id: str = ""


@dataclass
class Comment(ASTNode):
    """Comment line (# تعليق)"""
    text: str = ""


@dataclass
class PageBreak(ASTNode):
    """Manual page break (<<<)"""
    pass


@dataclass
class TextRun(ASTNode):
    """Text with inline formatting"""
    text: str = ""
    bold: bool = False
    italic: bool = False
    underline: bool = False
