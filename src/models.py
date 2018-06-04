from datetime import datetime

from peewee import *
from unipath import Path


cwd = Path(__file__).parent
db = SqliteDatabase(cwd.child('urls.db'))

LANGUAGES = (
    'ja-jp',
    'en',
    'zh-cn',
)


class BaseModel(Model):
    created = DateTimeField(null=False, default=datetime.now())
    updated = DateTimeField(null=False, default=datetime.now())

    class Meta:
        database = db


class Url(BaseModel):
    url = CharField(max_length=255, unique=True, null=False, index=True)
    priority = DecimalField(null=False, default=5.0)
    language = CharField(null=False, choices=LANGUAGES, max_length=10)

    class Meta:
        table_name = 'urls'

    def __str__(self):
        return self.url

    def create_xml(self):
        pass
