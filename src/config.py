import os

from unipath import Path


EXPORT_DIR = Path(__file__).ancestor(2).child('exports')
DB_PATH = EXPORT_DIR.child('urls.db')
XML_TEMPLATE_PATH = Path(__file__).ancestor(1).child('sitemap_template.xml')
XML_EXPORT_PATH = Path(os.environ.get('HOME'), 'Downloads')
