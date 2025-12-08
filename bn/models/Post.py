# /bn/models/Post.py

import peewee as pw
from . import BaseModel
from .Site import Site


class Post(BaseModel):
    
    id = pw.AutoField()
    title_src = pw.CharField()
    title_dest = pw.CharField()
    text_src = pw.CharField()
    text_dest = pw.CharField()
    pub_date = pw.DateTimeField()
    url = pw.CharField()
    site = pw.ForeignKeyField(Site, backref='posts', on_delete='CASCADE')

    class Meta:
        table_name = 'posts'


    def __repr__(self):
        return f'<Post {self.id} | {self.title_src[:30]}>'