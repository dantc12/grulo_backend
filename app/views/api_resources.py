from app.views.is_alive import IsAlive
from app.views.login_resource import Login
from app.views.posts_creator_resource import PostCreator
from app.views.dynamic_resources import PostById, GroupById, UserByName
from app.views.signup_resource import SignUp
from app.views.groups_resource import GetGroupByCoor, AddUserToGroup, GetAllGroups

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
        "name": PostCreator,
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
        "name": UserByName,
        "path": '/users/<string:username>'
    }
]
