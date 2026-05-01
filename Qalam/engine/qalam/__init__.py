"""
Qalam Language Engine - Main Package
A academic writing language compiler from .qlm to PDF/Word/HTML
"""

__version__ = "1.0.0"
__author__ = "Qalam Team"

from .lexer import QalamLexer
from .parser import QalamParser
from .ast_nodes import *
from .renderer_pdf import PDFRenderer
from .renderer_docx import DOCXRenderer
from .keywords import (
    ENVIRONMENTS_AR, ENVIRONMENTS_EN, ENVIRONMENTS_FR,
    SECTION_MARKERS_AR, SECTION_MARKERS_EN, SECTION_MARKERS_FR,
    METADATA_KEYS_AR, METADATA_KEYS_EN, METADATA_KEYS_FR,
)

__all__ = [
    'QalamLexer',
    'QalamParser', 
    'PDFRenderer',
    'DOCXRenderer',
    'ENVIRONMENTS_AR',
    'ENVIRONMENTS_EN',
    'ENVIRONMENTS_FR',
]
