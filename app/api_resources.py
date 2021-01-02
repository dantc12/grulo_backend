from app.views.authentication.is_alive import IsAlive
from app.views.authentication.login_resource import Login
from app.views.authentication.logout_resource import Logout
from app.views.posts_resource import PostsResource
from app.views.dynamic_resources.post_by_id import PostById
from app.views.dynamic_resources.users_by_name import UserByName
from app.views.dynamic_resources.groups_by_id import GroupById
from app.views.authentication.signup_resource import SignUp
from app.views.groups_resources.groups_resource import AddUserToGroup, GetAllGroups
from app.views.groups_resources.search_groups import SearchGroup
from app.views.groups_resources.group_by_coor import GetGroupByCoor

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