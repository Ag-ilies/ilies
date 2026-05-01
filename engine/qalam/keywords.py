"""
Keywords dictionary for Qalam language
Supports Arabic, English, and French
"""

class Keywords:
    """Multi-language keywords for Qalam"""
    
    # Document types / أنواع المستندات
    DOCUMENT_TYPES = {
        'ar': ['مذكرة', 'رسالة', 'أطروحة', 'بحث', 'مقال'],
        'en': ['memoir', 'thesis', 'dissertation', 'research', 'paper'],
        'fr': ['mémoire', 'thèse', 'doctorat', 'recherche', 'article']
    }
    
    # Metadata keys / مفاتيح البيانات الوصفية
    METADATA_KEYS = {
        'ar': {
            'عنوان': 'title',
            'طالب': 'student',
            'مشرف': 'supervisor',
            'جامعة': 'university',
            'كلية': 'faculty',
            'سنة': 'year',
            'درجة': 'degree',
            'لغة': 'language',
            'مخرج': 'output'
        },
        'en': {
            'title': 'title',
            'student': 'student',
            'supervisor': 'supervisor',
            'university': 'university',
            'faculty': 'faculty',
            'year': 'year',
            'degree': 'degree',
            'language': 'language',
            'output': 'output'
        },
        'fr': {
            'titre': 'title',
            'étudiant': 'student',
            'directeur': 'supervisor',
            'université': 'university',
            'faculté': 'faculty',
            'année': 'year',
            'diplôme': 'degree',
            'langue': 'language',
            'sortie': 'output'
        }
    }
    
    # Environment types / أنواع البيئات
    ENVIRONMENTS = {
        'ar': {
            'ملخص': 'abstract',
            'مقدمة': 'introduction',
            'خاتمة': 'conclusion',
            'إهداء': 'dedication',
            'شكر': 'acknowledgements',
            'اقتباس': 'quote',
            'تعريف': 'definition',
            'ملاحظة': 'note',
            'معادلة': 'equation',
            'شكل': 'figure',
            'جدول': 'table',
            'قائمة': 'list',
            'مراجع': 'references',
            'كتاب': 'book',
            'مقال': 'article',
            'مثال': 'example',
            'ملحق': 'appendix'
        },
        'en': {
            'abstract': 'abstract',
            'introduction': 'introduction',
            'conclusion': 'conclusion',
            'dedication': 'dedication',
            'acknowledgements': 'acknowledgements',
            'quote': 'quote',
            'definition': 'definition',
            'note': 'note',
            'equation': 'equation',
            'figure': 'figure',
            'table': 'table',
            'list': 'list',
            'references': 'references',
            'book': 'book',
            'article': 'article',
            'example': 'example',
            'appendix': 'appendix'
        },
        'fr': {
            'résumé': 'abstract',
            'introduction': 'introduction',
            'conclusion': 'conclusion',
            'dédicaces': 'dedication',
            'remerciements': 'acknowledgements',
            'citation': 'quote',
            'définition': 'definition',
            'note': 'note',
            'équation': 'equation',
            'figure': 'figure',
            'tableau': 'table',
            'liste': 'list',
            'bibliographie': 'references',
            'livre': 'book',
            'article': 'article',
            'exemple': 'example',
            'annexe': 'appendix'
        }
    }
    
    # Section markers / علامات الأقسام
    SECTION_MARKERS = {
        'ar': {
            'فصل': 'chapter',
            'قسم': 'section',
            'فرع': 'subsection'
        },
        'en': {
            'chapter': 'chapter',
            'section': 'section',
            'subsection': 'subsection'
        },
        'fr': {
            'chapitre': 'chapter',
            'section': 'section',
            'sous-section': 'subsection'
        }
    }
    
    # Degree types / أنواع الدرجات العلمية
    DEGREES = {
        'ar': ['ليسانس', 'ماستر', 'دكتوراه', 'ماجستير'],
        'en': ['bachelor', 'master', 'phd', 'doctorate'],
        'fr': ['licence', 'master', 'doctorat']
    }
    
    @classmethod
    def get_all_environments(cls):
        """Get all environment names in all languages"""
        envs = set()
        for lang_envs in cls.ENVIRONMENTS.values():
            envs.update(lang_envs.keys())
        return envs
    
    @classmethod
    def get_all_metadata_keys(cls):
        """Get all metadata keys in all languages"""
        keys = set()
        for lang_keys in cls.METADATA_KEYS.values():
            keys.update(lang_keys.keys())
        return keys
    
    @classmethod
    def normalize_environment(cls, name):
        """Normalize environment name to English"""
        name = name.strip()
        for lang_envs in cls.ENVIRONMENTS.values():
            if name in lang_envs:
                return lang_envs[name]
        return name.lower()
    
    @classmethod
    def normalize_metadata_key(cls, key):
        """Normalize metadata key to English"""
        key = key.strip()
        for lang_keys in cls.METADATA_KEYS.values():
            if key in lang_keys:
                return lang_keys[key]
        return key.lower()
    
    @classmethod
    def is_environment(cls, name):
        """Check if name is a valid environment"""
        return name.strip() in cls.get_all_environments()
    
    @classmethod
    def is_document_type(cls, name):
        """Check if name is a valid document type"""
        name = name.strip()
        for lang_types in cls.DOCUMENT_TYPES.values():
            if name in lang_types:
                return True
        return False
