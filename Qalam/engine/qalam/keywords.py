"""
Qalam Keywords - Trilingual support (Arabic, English, French)
"""

# Document types
DOC_TYPES_AR = ['مذكرة', 'رسالة', 'أطروحة', 'بحث', 'تقرير']
DOC_TYPES_EN = ['memoir', 'thesis', 'dissertation', 'paper', 'report']
DOC_TYPES_FR = ['mémoire', 'thèse', 'dissertation', 'article', 'rapport']

# Environment types
ENVIRONMENTS_AR = {
    'ملخص': 'abstract', 'مقدمة': 'introduction', 'خاتمة': 'conclusion',
    'إهداء': 'dedication', 'شكر': 'acknowledgements', 'اقتباس': 'quote',
    'تعريف': 'definition', 'ملاحظة': 'note', 'معادلة': 'equation',
    'شكل': 'figure', 'جدول': 'table', 'قائمة': 'list', 'مراجع': 'references',
    'كتاب': 'book', 'مقال': 'article', 'مثال': 'example', 'ملحق': 'appendix'
}

ENVIRONMENTS_EN = {
    'abstract': 'abstract', 'introduction': 'introduction', 'conclusion': 'conclusion',
    'dedication': 'dedication', 'acknowledgements': 'acknowledgements', 'quote': 'quote',
    'definition': 'definition', 'note': 'note', 'equation': 'equation',
    'figure': 'figure', 'table': 'table', 'list': 'list', 'references': 'references',
    'book': 'book', 'article': 'article', 'example': 'example', 'appendix': 'appendix'
}

ENVIRONMENTS_FR = {
    'résumé': 'abstract', 'introduction': 'introduction', 'conclusion': 'conclusion',
    'dédicaces': 'dedication', 'remerciements': 'acknowledgements', 'citation': 'quote',
    'définition': 'definition', 'note': 'note', 'équation': 'equation',
    'figure': 'figure', 'tableau': 'table', 'liste': 'list', 'bibliographie': 'references',
    'livre': 'book', 'article': 'article', 'exemple': 'example', 'annexe': 'appendix'
}

# Section markers
SECTION_MARKERS_AR = {'فصل': 'chapter', 'قسم': 'section', 'فرع': 'subsection'}
SECTION_MARKERS_EN = {'chapter': 'chapter', 'section': 'section', 'subsection': 'subsection'}
SECTION_MARKERS_FR = {'chapitre': 'chapter', 'section': 'section', 'sous-section': 'subsection'}

# Metadata keys
METADATA_KEYS_AR = {
    'عنوان': 'title', 'طالب': 'student', 'مشرف': 'supervisor',
    'جامعة': 'university', 'كلية': 'faculty', 'سنة': 'year',
    'درجة': 'degree', 'لغة': 'language', 'مخرج': 'output',
    'تخصص': 'specialty', 'قسم': 'department'
}

METADATA_KEYS_EN = {
    'title': 'title', 'student': 'student', 'supervisor': 'supervisor',
    'university': 'university', 'faculty': 'faculty', 'year': 'year',
    'degree': 'degree', 'language': 'language', 'output': 'output',
    'specialty': 'specialty', 'department': 'department'
}

METADATA_KEYS_FR = {
    'titre': 'title', 'étudiant': 'student', 'directeur': 'supervisor',
    'université': 'university', 'faculté': 'faculty', 'année': 'year',
    'diplôme': 'degree', 'langue': 'language', 'sortie': 'output',
    'spécialité': 'specialty', 'département': 'department'
}

# Combined keyword sets for detection
ALL_ENVIRONMENTS = set(ENVIRONMENTS_AR.keys()) | set(ENVIRONMENTS_EN.keys()) | set(ENVIRONMENTS_FR.keys())
ALL_SECTION_MARKERS = set(SECTION_MARKERS_AR.keys()) | set(SECTION_MARKERS_EN.keys()) | set(SECTION_MARKERS_FR.keys())
ALL_METADATA_KEYS = set(METADATA_KEYS_AR.keys()) | set(METADATA_KEYS_EN.keys()) | set(METADATA_KEYS_FR.keys())

# Helper functions
def normalize_env(env_name):
    """Normalize environment name to English"""
    env_name = env_name.strip()
    if env_name in ENVIRONMENTS_AR:
        return ENVIRONMENTS_AR[env_name]
    if env_name in ENVIRONMENTS_EN:
        return ENVIRONMENTS_EN[env_name]
    if env_name in ENVIRONMENTS_FR:
        return ENVIRONMENTS_FR[env_name]
    return env_name.lower()

def normalize_section(marker):
    """Normalize section marker to English"""
    marker = marker.strip()
    if marker in SECTION_MARKERS_AR:
        return SECTION_MARKERS_AR[marker]
    if marker in SECTION_MARKERS_EN:
        return SECTION_MARKERS_EN[marker]
    if marker in SECTION_MARKERS_FR:
        return SECTION_MARKERS_FR[marker]
    return marker.lower()

def normalize_metadata(key):
    """Normalize metadata key to English"""
    key = key.strip()
    if key in METADATA_KEYS_AR:
        return METADATA_KEYS_AR[key]
    if key in METADATA_KEYS_EN:
        return METADATA_KEYS_EN[key]
    if key in METADATA_KEYS_FR:
        return METADATA_KEYS_FR[key]
    return key.lower()
