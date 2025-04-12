import os
from datetime import datetime
from pathlib import Path
import frontmatter
import markdown

class BlogPost:
    def __init__(self, title, content, date, description, author, slug):
        self.title = title
        self.content = content
        self.date = date
        self.description = description
        self.author = author
        self.slug = slug

def get_blog_posts():
    """Get all blog posts sorted by date."""
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
                extensions=['extra', 'codehilite']
            )
            
            # Create slug from filename (remove date and extension)
            slug = file.stem.split('-', 3)[-1]
            
            # Create BlogPost object
            blog_post = BlogPost(
                title=post.get('title', 'Untitled'),
                content=html_content,
                date=post.get('date', datetime.now().date()),
                description=post.get('description', ''),
                author=post.get('author', 'Anonymous'),
                slug=slug
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
                extensions=['extra', 'codehilite']
            )
            
            return BlogPost(
                title=post.get('title', 'Untitled'),
                content=html_content,
                date=post.get('date', datetime.now().date()),
                description=post.get('description', ''),
                author=post.get('author', 'Anonymous'),
                slug=slug
            )
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    return None 