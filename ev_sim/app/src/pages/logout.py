import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_login import logout_user, current_user

dash.register_page(__name__)


def layout():
    if current_user.is_authenticated:
        logout_user()
    return dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Logout"),
                            html.P(
                                "You have been logged out - You will be redirected to login"
                            ),
                            dcc.Interval(
                                id={"index": "redirectLogin", "type": "redirect"},
                                n_intervals=0,
                                interval=1 * 3000,
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
