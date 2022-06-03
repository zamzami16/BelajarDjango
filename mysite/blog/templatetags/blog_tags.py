from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=3):
    """
    get latest posts with default 3 latest posts
    """
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}

@register.simple_tag
def get_most_commented_posts(count=3):
    """
    get most commented posts with default 3 most commented posts
    """
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]

@register.filter(name="markdown")
def markdown_format(text):
    """
    convert text to markdown format
    """
    return mark_safe(markdown.markdown(text))
