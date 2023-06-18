from dash import Input, Output, ALL, no_update
from flask_login import current_user
from flask import session
from plots.test import test


from utils.login_handler import restricted_page
from config import settings


def callbacks(app):
    @app.callback(
        Output("url", "pathname"),
        Input("url", "pathname"),
        Input({"index": ALL, "type": "redirect"}, "n_intervals"),
    )
    def update_authentication_status(path, n_intervals):
        """Update authentication status."""
        # logout redirect
        if n_intervals:
            if not n_intervals[0]:
                return no_update
            return "/login"

        # test if user is logged in
        if current_user.is_authenticated:
            if path == "/login":
                return "/"
            return no_update
        else:
            # if page is restricted, redirect to login and save path
            if path in restricted_page:
                session["url"] = path
                return "/login"

        # if path not login and logout display login link
        if current_user and path not in ["/login", "/logout"]:
            return no_update

        # if path login and logout hide links
        if path in ["/login", "/logout"]:
            return no_update
