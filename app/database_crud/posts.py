from typing import List, Optional

from .. import exceptions, schemas, models
from . import users, groups


def get_post_by_id(post_id: str) -> models.Post:
    if models.Post.objects(post_id=post_id):
        return models.Post.objects(post_id=post_id)[0]
    raise exceptions.PostNotFound(post_id)


# TODO add edit post


def add_comment_to_post(post_id: str, comment: schemas.CommentCreate) -> models.Post:
    post = get_post_by_id(post_id)
    created_comment = schemas.Comment(index=len(post.comments),
                                      likes=[],
                                      **comment.dict())
    post.comments.append(created_comment.dict())
    post.save()
    return post


def create_post(post: schemas.PostCreate) -> models.Post:
    posting_user = users.get_user_by_name(username=post.username)
    posted_group = groups.get_group_by_name(group_name=post.group_name)
    taken_post_ids = [post.post_id for post in models.Post.objects]
    post_id = 1
    while str(post_id) in taken_post_ids:
        post_id += 1
    post_id = str(post_id)
    post = models.Post(post_id=post_id, **post.dict())
    post.save()

    # add to user's posts
    posting_user.update(post_ids=posting_user.post_ids + [post_id])
    # add to group's posts
    posted_group.update(post_ids=posted_group.post_ids + [post_id])

    return post


def get_posts_for_user(username: str, limit: Optional[int] = None) -> List[models.Post]:
    user = users.get_user_by_name(username)
    posts = []
    for group_id in user.group_ids:
        group = groups.get_group_by_id(group_id)
        group_posts = [get_post_by_id(post_id) for post_id in group.post_ids]
        if limit is not None and len(posts) + len(group_posts) > limit:
            i = 0
            while len(posts) < limit:
                posts.append(group_posts[i])
                i += 1
            return posts
        else:
            posts.extend(group_posts)
    return posts


def get_posts_by_user(username: str) -> List[models.Post]:
    user = users.get_user_by_name(username)
    return [get_post_by_id(post_id) for post_id in user.post_ids]


def get_posts_by_group_name(group_name: str) -> List[models.Post]:
    group = groups.get_group_by_name(group_name)
    return [get_post_by_id(post_id) for post_id in group.post_ids]


def get_posts_by_group_id(group_id: str) -> List[models.Post]:
    group = groups.get_group_by_id(group_id)
    return [get_post_by_id(post_id) for post_id in group.post_ids]

# TODO add get posts by coordinates
