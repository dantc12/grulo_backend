from app.views.is_alive import IsAlive
from app.views.login_resource import Login
from app.views.posts_resource import PostsResource
from app.views.signup_resource import SignUp

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
        "name": PostsResource,
        "path": '/posts'
    }
]
