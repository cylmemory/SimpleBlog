from .. import db
from ..useraccounts.models import User
import markdown2 as Markdown, bleach
import datetime


post_status = ((0, 'post'), (1, 'draft'))


def get_clean_html_content(html_content):
    allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'hr', 'img',
                        'table', 'thead', 'tbody', 'tr', 'th', 'td',
                        'sup', 'sub']
    allow_attrs = {'*': ['class'],
                'a': ['href', 'rel', 'name'],
                'img': ['alt', 'src', 'title'], }
    html_content = bleach.linkify(bleach.clean(html_content, tags=allow_tags, attributes=allow_attrs, strip=True))
    return html_content


class Post(db.Document):
    title = db.StringField(max_length=255, required=True, default='New blog')
    abstract = db.StringField()
    content = db.StringField(required=True)
    content_html = db.StringField(required=True)
    author = db.ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=64))
    category = db.StringField(max_length=64)
    status = db.IntField(required=True, choices=post_status, default=0)
    create_time = db.DateTimeField()
    modify_time = db.DateTimeField()

    '''rewrite save method.'''
    def save(self, allow_set_time=False, *args, **kwargs):
        if not allow_set_time:
            time = datetime.datetime.utcnow()
            if not self.create_time:
                self.create_time = time
            self.modify_time = time

        self.content_html = Markdown.markdown(self.content, extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.content_html = get_clean_html_content(self.content_html)

        return super(Post, self).save(*args, **kwargs)

