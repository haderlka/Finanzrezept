from django import template
from django.utils.safestring import mark_safe
import markdown
import re

register = template.Library()

@register.filter(name='markdown_with_blocks')
def markdown_with_blocks(value):
    """
    Convert markdown to HTML with support for special blockquotes.
    
    Usage in template:
    {{ content|markdown_with_blocks }}
    """
    if not value:
        return ""
    
    # Convert markdown to HTML
    html = markdown.markdown(value, extensions=['fenced_code', 'codehilite'])
    
    # Add data-type attribute to blockquotes based on their content
    def process_blockquote(match):
        content = match.group(1)
        if content.startswith('Hint:'):
            return f'<blockquote data-type="hint">{content[5:]}</blockquote>'
        elif content.startswith('Rule:'):
            return f'<blockquote data-type="rule">{content[5:]}</blockquote>'
        elif content.startswith('Warning:'):
            return f'<blockquote data-type="warning">{content[8:]}</blockquote>'
        elif content.startswith('Info:'):
            return f'<blockquote data-type="info">{content[5:]}</blockquote>'
        else:
            return f'<blockquote>{content}</blockquote>'
    
    # Process blockquotes
    html = re.sub(r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>', 
                 process_blockquote, 
                 html, 
                 flags=re.DOTALL)
    
    return mark_safe(html) 