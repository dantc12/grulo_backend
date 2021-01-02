from app.views.is_alive import IsAlive
from app.views.login_resource import Login
from app.views.logout_resource import Logout
from app.views.posts_resource import PostsResource
from app.views.dynamic_resources.dynamic_resources import PostById
from app.views.dynamic_resources.users_by_name import UserByName
from app.views.dynamic_resources.groups_by_id import GroupById
from app.views.signup_resource import SignUp
from app.views.groups_resource import GetGroupByCoor, AddUserToGroup, GetAllGroups, SearchGroup

api_resources = [
    {
        "name": IsAlive,
        "path": '/'
    },
    {
        "name": Login,
        "path": '/login'
    },
    {
        "name": SignUp,
        "path": '/signup'
    },
    {
        "name": Logout,
        "path": '/logout'
    },
    {
        "name": PostsResource,
        "path": '/posts'
    },
    {
        "name": GetGroupByCoor,
        "path": '/groups/getByCoor'
    },
    {
        "name": AddUserToGroup,
        "path": '/groups/AddUser'
    },
    {
        "name": GetAllGroups,
        "path": '/groups'
    },
    {
        "name": PostById,
        "path": '/posts/<int:post_id>'
    },
    {
        "name": GroupById,
        "path": '/groups/<string:groupid>'
    },
    {
        "name": SearchGroup,
        "path": '/groups/search'
    },
    {
        "name": UserByName,
        "path": '/users/<string:username>'
    }
]
