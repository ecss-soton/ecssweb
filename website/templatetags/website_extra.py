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
    """Sort which also allows None."""
    return l.order_by(key)


@register.filter
def shuffle(l):
    l = list(l)
    random.shuffle(l)
    return l


@register.filter
def md(s):
    """Transform Markdown into html.
       Not allowed html tags will be escaped.
    """
    cleaner = Cleaner(tags=markdown_allowed_tags, filters=[partial(LinkifyFilter, parse_email=True)])
    return cleaner.clean(markdown.markdown(s))


@register.filter
def md_nourl(s):
    """Transform Markdown into html. URLs and email addresses are not converted into links automatically.
       Not allowed html tags will be escaped.
    """
    cleaner = Cleaner(tags=markdown_allowed_tags)
    return cleaner.clean(markdown.markdown(s))


@register.simple_tag(takes_context=True)
def update_query(context, **kwargs):
    """Construct an URL contains only the querystring (excluding "?") by updating the current URL's querystring with the provided arguments."""
    request = context['request']
    query = request.GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def has_group(user, group_name):
    """Check if a user is in a specific group."""
    return user.groups.filter(name=group_name).exists()