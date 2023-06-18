"""Layout for the app."""
from dash import html, dcc, page_container
import dash_bootstrap_components as dbc
from config import settings


def get_layout():
    layout = html.Div(
        [
            dcc.Location(id="url"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [_get_app_header()],
                                style={
                                    "height": "50px",
                                    "backgroundColor": "white",
                                    "position": "fixed",
                                    "right": "1vw",
                                    "left": "1vw",
                                },
                            ),
                            dbc.Row([page_container], style={"paddingTop": "10px"}),
                        ],
                    ),
                ],
            ),
        ],
        style={"padding": "10px 30px 10px 30px"},
    )
    return layout


def _get_app_header():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="https://axle.energy/static/images/logo-monochrome%20white.png",
                                height="36px",
                            ),
                            width="auto",
                            style={
                                "borderRight": "2px solid #bc342c",
                                "paddingRight": "18px",
                            },
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "AXLE EV SIMULATOR",
                                style={
                                    "fontWeight": "bold",
                                    "paddingLeft": "20px",
                                    "color": "white",
                                },
                            ),
                            style={
                                "paddingLeft": "5px",
                                "display": "contents",
                            },
                        ),
                        dbc.Col(
                            "Version: " + settings.VERSION,
                            style={
                                "color": "white",
                                "display": "flex",
                                "fontSize": "0.8rem",
                                "justifyContent": "right",
                                "alignItems": "center",
                            },
                        ),
                    ],
                    style={"width": "100%"},
                ),
            ],
            fluid=True,
        ),
        color="dark",
    )
