from app.views.is_alive import IsAlive
from app.views.login_resource import Login
from app.views.posts_creator_resource import PostCreator
from app.views.dynamic_resources import PostById, GroupById
from app.views.signup_resource import SignUp
from app.views.groups_resource import GetByCoor, AddUser

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
        "name": PostById,
        "path": '/posts/<int:post_id>'
    },
    {
        "name": GetByCoor,
        "path": '/groups/getByCoor'
    },
    {
        "name": AddUser,
        "path": '/groups/AddUser'
    },
    {
        "name": GroupById,
        "path": '/groups/<string:groupid>'
    }
]
