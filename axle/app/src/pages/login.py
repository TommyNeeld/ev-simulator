import dash
import dash_bootstrap_components as dbc
from dash import html


dash.register_page(__name__)


# Login screen
def layout():
    return dbc.Col(
        [
            dbc.Row(
                [
                    html.H3("Login"),
                    html.P("Please log in to continue:"),
                    html.Form(
                        [
                            dbc.Col(
                                [
                                    dbc.Input(
                                        placeholder="Enter your username",
                                        type="text",
                                        id="uname-box",
                                        name="username",
                                        style={"marginTop": "5px"},
                                    ),
                                    dbc.Input(
                                        placeholder="Enter your password",
                                        type="password",
                                        id="pwd-box",
                                        name="password",
                                        style={"marginTop": "5px"},
                                    ),
                                    dbc.Button(
                                        children="Login",
                                        n_clicks=0,
                                        type="submit",
                                        id="login-button",
                                        style={"marginTop": "5px"},
                                    ),
                                ],
                                width=4,
                            ),
                            html.Div(children="", id="output-state"),
                        ],
                        method="POST",
                    ),
                ]
            ),
        ],
        style={
            "top": "100px",
            "bottom": "10px",
            "overflowY": "scroll",
            "overflowX": "clip",
            "position": "fixed",
            "left": "22vw",
            "right": "1vw",
        },
    )
