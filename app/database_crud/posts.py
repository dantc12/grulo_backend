from typing import List, Optional

from . import users, groups, models
from .. import exceptions, schemas


def get_post_by_id(post_id: str) -> models.Post:
    post = models.Post.objects(post_id=post_id).first()
    if post is not None:
        return post
    raise exceptions.PostNotFound(post_id)


def add_comment_to_post(post_id: str, comment: schemas.CommentCreate, user: models.User) -> models.Post:
    post = get_post_by_id(post_id)
    created_comment = schemas.Comment(index=len(post.comments),
                                      likes=[],
                                      username=user.username,
                                      **comment.dict())
    post.comments.append(created_comment.dict())
    post.save()
    return post


def create_post(post: schemas.PostCreate, posting_user: models.User) -> models.Post:
    posted_group = groups.get_group_by_name(group_name=post.group_name)
    if posting_user.username not in posted_group.users:
        raise exceptions.NotMember(posting_user.username, posted_group.group_name)
    taken_post_ids = [post.post_id for post in models.Post.objects]
    post_id = 1
    while str(post_id) in taken_post_ids:
        post_id += 1
    post_id = str(post_id)
    post = models.Post(post_id=post_id, username=posting_user.username, **post.dict())
    post.save()

    # add to user's posts
    posting_user.update(post_ids=posting_user.post_ids + [post_id])
    # add to group's posts
    posted_group.update(post_ids=posted_group.post_ids + [post_id])

    return post


def get_user_feed(user: models.User) -> List[models.Post]:
    posts = []
    for group_name in user.groups:
        posts.extend(get_posts_by_group_name(group_name))
    return posts


def get_posts_by_user(username: str) -> List[models.Post]:
    user = users.get_user_by_name(username)
    return [get_post_by_id(post_id) for post_id in user.post_ids]


def get_posts_by_group_name(group_name: str) -> List[models.Post]:
    group = groups.get_group_by_name(group_name)
    return [get_post_by_id(post_id) for post_id in group.post_ids]
