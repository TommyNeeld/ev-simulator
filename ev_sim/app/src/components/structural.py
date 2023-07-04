from dash import html
import dash_bootstrap_components as dbc


def create_divider(color="#0000FF", boarderWidth="0.3vh"):
    return dbc.Col(
        html.Hr(
            style={
                "borderWidth": boarderWidth,
                "width": "100%",
                "borderColor": color,
                "borderStyle": "solid",
            }
        ),
        width=12,
    )
