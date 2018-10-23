from .. import db
from ..useraccounts.models import User
import markdown2 as Markdown, bleach
import datetime, hashlib, urllib

post_status = ((0,
                'post'), (1, 'draft'))


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

    '''override save method.'''
    def save(self, allow_set_time=False, *args, **kwargs):
        if not allow_set_time:
            time = datetime.datetime.utcnow()
            if not self.create_time:
                self.create_time = time
            self.modify_time = time

        self.content_html = Markdown.markdown(self.content, extras=['code-friendly', 'fenced-code-blocks', 'tables'])
        self.content_html = get_clean_html_content(self.content_html)

        return super(Post, self).save(*args, **kwargs)

    def post_to_dict(self):
        dict_post ={}

        dict_post['title'] = self.title
        dict_post['abstract'] = self.abstract
        dict_post['content'] = self.content
        dict_post['author'] = self.author
        dict_post['tags'] = self.tags
        dict_post['category'] = self.category
        dict_post['status'] = self.status
        dict_post['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M')
        dict_post['modify_time'] = self.modify_time.strftime('%Y-%m-%d %H:%M')

        return dict_post

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Comment(db.Document):
    post_id = db.StringField()
    post_title = db.StringField()
    author = db.StringField(required=True)
    email = db.EmailField(max_length=255)
    body = db.StringField()
    body_html = db.StringField()
    create_time = db.DateTimeField()
    disabled = db.BooleanField(default=True)
    replay_to = db.ReferenceField('self')
    gavatar_id = db.StringField(default='00000000000')

    def save(self, *args, **kwargs):
        if self.body:
            body_html = Markdown.markdown(self.body, extras=['code-friendly', 'fenced-code-blocks', 'tables'])
            self.body_html = get_clean_html_content(body_html)

        if self.email:
            self.gavatar_id = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

        if not self.create_time:
            self.create_time = datetime.datetime.now()

        return super(Comment, self).save(*args, **kwargs)

    def get_gavatar_url(self):
        gavatar_url = '//s.gravatar.com/avatar/' + self.gavatar_id
        gavatar_url = gavatar_url + '?s=40'
        return gavatar_url

    def comment_to_dict(self):
        dict_comment = {}

        dict_comment['post_id'] = self.post_id
        dict_comment['post_title'] = self.post_title
        dict_comment['author'] = self.author
        dict_comment['email'] = self.email
        dict_comment['body'] = self.body
        dict_comment['create_time'] = self.create_time.strftime('%Y-%m-%d %H:%M')
        dict_comment['disabled'] = self.disabled
        dict_comment['gavatar_id'] = self.gavatar_id
        dict_comment['replay_to'] = self.replay_to

        return dict_comment

    def __unicode__(self):
        return self.body[:64]

    meta = {
        'ordering': ['-create_time']
    }


class PostStatistics(db.Document):
    post = db.ReferenceField(Post)
    visit_count = db.IntField(default=0)
    verbose_count_base = db.IntField(default=0)


class Tracker(db.Document):
    post = db.ReferenceField(Post)
    ip = db.StringField()
    user_agent = db.StringField()
    create_time = db.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        return super(Tracker, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.ip

    meta = {
        'allow_inheritance': True,
        'indexes': ['ip'],
        'ordering': ['-create_time']
    }