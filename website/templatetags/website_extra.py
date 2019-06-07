from django import template
import random
import markdown
from bleach import Cleaner
from bleach.linkifier import LinkifyFilter
from functools import partial


markdown_allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul', 'p']


register = template.Library()


@register.filter
def msort(l, key):
    return l.order_by(key)


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def shuffle(l):
    l = list(l)
    random.shuffle(l)
    return l

@register.filter
def md(s):
    cleaner = Cleaner(tags=markdown_allowed_tags, filters=[partial(LinkifyFilter, parse_email=True)])
    return cleaner.clean(markdown.markdown(s))


@register.filter
def md_nourl(s):
    cleaner = Cleaner(tags=markdown_allowed_tags)
    return cleaner.clean(markdown.markdown(s))
