from peewee import *

from . import config


# Export directory
export_dir = config.EXPORT_DIR
if not export_dir.exists():
    export_dir.mkdir()

# Database path
db = SqliteDatabase(config.DB_PATH)

# Language choices
LANGUAGES = (
    'ja-jp',
    'en',
    'zh-cn',
    'ko-kr',
)


class BaseModel(Model):
    """Timestamped abstract model"""
    created = DateTimeField(null=False)
    updated = DateTimeField(null=False)

    class Meta:
        database = db


class Url(BaseModel):
    """The URL model"""
    url = CharField(max_length=255, unique=True, null=False, index=True)
    referer = CharField(max_length=255, null=False, default='', index=True)
    priority = DecimalField(null=False, default=5.0)
    language = CharField(null=False, choices=LANGUAGES, max_length=10)

    class Meta:
        table_name = 'urls'

    def __str__(self):
        return self.url
