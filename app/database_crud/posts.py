from typing import List

from . import users, groups, models
from .. import exceptions, schemas


def get_post_by_id(id: str) -> models.Post:
    post = models.Post.objects(id=id).first()
    if post is not None:
        return post
    raise exceptions.PostNotFound(id)


def add_comment_to_post(post_id: str, comment: schemas.CommentCreate, user: models.User) -> models.Post:
    post = get_post_by_id(post_id)
    created_comment = schemas.Comment(index=len(post.comments),
                                      likes=[],
                                      user=user.id,
                                      **comment.dict())
    post.comments.append(created_comment.dict())
    post.save()
    return post


def like_post(post_id: str, user: models.User) -> models.Post:
    post = get_post_by_id(post_id)
    if user.id not in post.likes:
        post.likes.append(user.id)
        post.save()
    return post


def unlike_post(post_id: str, user: models.User) -> models.Post:
    post = get_post_by_id(post_id)
    if user.id in post.likes:
        post.likes.remove(user.id)
        post.save()
    return post


def create_post(post: schemas.PostCreate, posting_user: models.User) -> models.Post:
    posted_group = groups.get_group_by_id(post.group)
    if posting_user.id not in posted_group.users:
        raise exceptions.NotMember(str(posting_user.id), str(posted_group.id))
    post = models.Post(user=posting_user.id, **post.dict())
    post.save()

    # add to user's posts
    posting_user.update(posts=posting_user.posts + [post.id])
    # add to group's posts
    posted_group.update(posts=posted_group.posts + [post.id])

    return post


def get_user_feed(user: models.User) -> List[models.Post]:
    posts = []
    for group_id in user.groups:
        posts.extend(get_posts_of_group(group_id))
    return posts


def get_posts_of_user(user_id: str) -> List[models.Post]:
    user = users.get_user_by_id(user_id)
    return [get_post_by_id(post_id) for post_id in user.posts]


def get_posts_of_group(group_id: str) -> List[models.Post]:
    group = groups.get_group_by_id(group_id)
    return [get_post_by_id(post_id) for post_id in group.posts]
