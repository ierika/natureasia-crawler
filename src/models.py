from peewee import *
from unipath import Path


cwd = Path(__file__).parent
db = SqliteDatabase(cwd.child('urls.db'))

LANGUAGES = (
    'ja-jp',
    'en',
    'zh-cn',
    'ko-kr',
)


class BaseModel(Model):
    created = DateTimeField(null=False)
    updated = DateTimeField(null=False)

    class Meta:
        database = db


class Url(BaseModel):
    url = CharField(max_length=255, unique=True, null=False, index=True)
    referer = CharField(max_length=255, null=False, default='', index=True)
    priority = DecimalField(null=False, default=5.0)
    language = CharField(null=False, choices=LANGUAGES, max_length=10)

    class Meta:
        table_name = 'urls'

    def __str__(self):
        return self.url
