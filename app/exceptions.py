class NotFoundException(Exception):
    def __init__(self, name: str):
        super().__init__(f"{name} not found.")


class UserNotFound(NotFoundException):
    def __init__(self, username: str):
        super().__init__(f"User {username}")


class PostNotFound(NotFoundException):
    def __init__(self, post_id: str):
        super().__init__(f"Post {post_id}")


class PostCommentNotFound(NotFoundException):
    def __init__(self, post_id: str, comment_index: int):
        super().__init__(f"Comment at index {comment_index} of post {post_id}")


class GroupNotFound(NotFoundException):
    def __init__(self, group_id: str):
        super().__init__(f"Group {group_id}")


class QueriedGroupNotFound(NotFoundException):
    def __init__(self, group_id: str):
        super().__init__(f"Queried Group {group_id}")


class AlreadyExistsException(Exception):
    def __init__(self, name: str):
        super().__init__(f"{name} already exists.")


class UserAlreadyExists(NotFoundException):
    def __init__(self, username: str):
        super().__init__(f"User {username}")


class PostAlreadyExists(NotFoundException):
    def __init__(self, post_id: str):
        super().__init__(f"Post {post_id}")


class GroupAlreadyExists(NotFoundException):
    def __init__(self, group_id: str):
        super().__init__(f"Group {group_id}")


class NotMember(Exception):
    def __init__(self, username: str, group_name: str):
        super().__init__(f"User {username} not member of group {group_name}.")


class BadInput(Exception):
    def __init__(self):
        super().__init__(f"Received bad input.")
