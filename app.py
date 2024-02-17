from datetime import datetime
from uuid import uuid4 as uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional

app = FastAPI()

posts=[]

# Post model    
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    create_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False

@app.get('/')
def read_root():
    return {'root':'Hello'}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/post')
def save_post(post:Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return post[-1]

@app.get('/post/{post_id}')
def get_post_id(post_id:str):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail='post not foud')

@app.delete('/post/{post_id}')
def delete_post_id(post_id:str):
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            return {'message','Post delete sucessfully'}
    raise HTTPException(status_code=404, detail='post not foud')

@app.put('/post/{post_id}')
def put_post_id(post_id:str, updatePost:Post):
    for post in posts:
        if post['id'] == post_id:
            post['title'] = updatePost.title
            post['author'] = updatePost.author
            post['content'] = updatePost.content
            post['published'] = updatePost.published
            return {'message','Post update sucessfully'}
    raise HTTPException(status_code=404, detail='post not foud')
