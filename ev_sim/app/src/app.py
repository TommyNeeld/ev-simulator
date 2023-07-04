"""
dash app for  EV simulator
auth using multi-page flask login - https://github.com/AnnMarieW/dash-multi-page-app-demos/tree/main/multi_page_flask_login
"""
from flask import Flask, request, redirect, session
from flask_login import login_user, LoginManager, UserMixin

from dash import Dash
import dash_bootstrap_components as dbc
from layout import get_layout
from callbacks import callbacks
from config import settings

# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@server.route("/login", methods=["POST"])
def login_button_click():
    if request.form:
        username = request.form["username"]
        password = request.form["password"]
        if settings.VALID_USERNAME_PASSWORD_PAIRS.get(username) is None:
            return (
                """invalid username and/or password <a href='/login'>login here</a>"""
            )
        if settings.VALID_USERNAME_PASSWORD_PAIRS.get(username) == password:
            login_user(User(username))
            if "url" in session:
                if session["url"]:
                    url = session["url"]
                    session["url"] = None
                    return redirect(url)  ## redirect to target url
            return redirect("/")  ## redirect to home
        return """invalid username and/or password <a href='/login'>login here</a>"""


app = Dash(
    __name__,
    server=server,
    title="EV Simulator",
    external_stylesheets=[dbc.themes.DARKLY, settings.CUSTOM_CSS],
    use_pages=True,
    suppress_callback_exceptions=True,
)

# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=settings.SECRET_KEY)

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


@login_manager.user_loader
def load_user(username):
    """
    This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)


app.layout = get_layout()

callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, port="8080")
