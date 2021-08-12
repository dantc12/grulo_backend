class _NotFoundException(Exception):
    def __init__(self, name: str):
        super().__init__(f"{name} not found.")


class UserNotFound(_NotFoundException):
    def __init__(self, username: str):
        super().__init__(f"User {username}")


class PostNotFound(_NotFoundException):
    def __init__(self, post_id: str):
        super().__init__(f"Post {post_id}")


class GroupNotFound(_NotFoundException):
    def __init__(self, group_id: str):
        super().__init__(f"Group {group_id}")
