class _NotFoundException(Exception):
    def __init__(self, name: str):
        self.msg = f"{name} not found."


class UserNotFound(_NotFoundException):
    def __init__(self, username: str):
        super().__init__(username)
        self.msg = "User " + self.msg


class PostNotFound(_NotFoundException):
    def __init__(self, post_id: str):
        super().__init__(post_id)
        self.msg = "Post " + self.msg


class GroupNotFound(_NotFoundException):
    def __init__(self, group_name: str):
        super().__init__(group_name)
        self.msg = "Group " + self.msg
