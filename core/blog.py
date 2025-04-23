import os
from datetime import datetime
from pathlib import Path
import frontmatter
import markdown
from collections import defaultdict
from mdx_math import MathExtension

class BlogPost:
    def __init__(self, title, content, date, description, author, slug, tags):
        self.title = title
        self.content = content
        self.date = date
        self.description = description
        self.author = author
        self.slug = slug
        self.tags = tags

def get_blog_posts(tags=None):
    """Get all blog posts sorted by date, optionally filtered by tags."""
    posts = []
    blog_dir = Path('content/blog')
    
    if not blog_dir.exists():
        return []
    
    for file in blog_dir.glob('*.md'):
        try:
            post = frontmatter.load(file)
            
            # Convert markdown content to HTML
            html_content = markdown.markdown(
                post.content,
                extensions=[
                    'extra',
                    'codehilite',
                    'attr_list',
                    MathExtension(enable_dollar_delimiter=True, add_preview=True)
                ],
                output_format='html5'
            )
            
            # Create slug from filename (remove date and extension)
            slug = file.stem.split('-', 3)[-1]
            
            # Get tags, default to empty list if not present
            post_tags = post.get('tags', [])
            
            # Skip if tag filter is set and post doesn't have all the required tags
            if tags and not all(tag in post_tags for tag in tags):
                continue
            
            # Create BlogPost object
            blog_post = BlogPost(
                title=post.get('title', 'Untitled'),
                content=html_content,
                date=post.get('date', datetime.now().date()),
                description=post.get('description', ''),
                author=post.get('author', 'Anonymous'),
                slug=slug,
                tags=post_tags
            )
            posts.append(blog_post)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    # Sort posts by date, newest first
    return sorted(posts, key=lambda x: x.date, reverse=True)

def get_post_by_slug(slug):
    """Get a specific blog post by its slug."""
    blog_dir = Path('content/blog')
    
    if not blog_dir.exists():
        return None
    
    # Look for files that end with the slug
    for file in blog_dir.glob(f'*-{slug}.md'):
        try:
            post = frontmatter.load(file)
            html_content = markdown.markdown(
                post.content,
                extensions=[
                    'extra',
                    'codehilite',
                    'attr_list',
                    MathExtension(enable_dollar_delimiter=True, add_preview=True)
                ],
                output_format='html5'
            )
            
            return BlogPost(
                title=post.get('title', 'Untitled'),
                content=html_content,
                date=post.get('date', datetime.now().date()),
                description=post.get('description', ''),
                author=post.get('author', 'Anonymous'),
                slug=slug,
                tags=post.get('tags', [])
            )
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    return None

def get_all_tags():
    """Get all unique tags and their counts."""
    tags = defaultdict(int)
    for post in get_blog_posts():
        for tag in post.tags:
            tags[tag] += 1
    return dict(tags) 