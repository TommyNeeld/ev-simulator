from dash import Input, Output, State, ALL, no_update
from flask_login import current_user
from flask import session
from plots.distribution import distributions
from plots.aggregate import aggregate
from simulation.parametric import run_monte_carlo
import pandas as pd
import numpy as np

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

    @app.callback(
        Output("number-of-evs-slider-output", "children"),
        Input("number-of-evs-slider", "value"),
    )
    def update_number_of_evs_slider_output(value):
        """Update number of EVs slider output."""
        return f"Number of EVs: {value}"

    @app.callback(
        Output("number-of-iterations-slider-output", "children"),
        Input("number-of-iterations-slider", "value"),
    )
    def update_number_of_iterations_slider_output(value):
        """Update number of iterations slider output."""
        return f"Number of iterations: {value}"

    # run the simulation
    @app.callback(
        Output("simulation-plug-in-histograms-graph", "figure"),
        Output("simulation-plug-out-histograms-graph", "figure"),
        Output("simulation-soc-graph", "figure"),
        Output("simulation-aggregate-graph", "figure"),
        Input("run-simulation-button", "n_clicks"),
        State("number-of-evs-slider", "value"),
        State("number-of-iterations-slider", "value"),
    )
    def update_simulation_results_graph(n_clicks, no_of_users, no_of_iterations):
        repeatable = False

        # TODO - get from table
        USER_GROUPS = {
            "Average (UK)": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.68,
                "soc-std": 0.3,
                "proportion": 0.4,
            },
            "Intel Octopus": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.52,
                "soc-std": 0.3,
                "proportion": 0.3,
            },
            "Infrequent C": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.18,
                "soc-std": 0.3,
                "proportion": 0.1,
            },
            "Infrequent D": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.73,
                "soc-std": 0.3,
                "proportion": 0.1,
            },
            "Scheduled": {
                "pi-mean": 22,
                "pi-std": 1,
                "po-mean": 9,
                "po-std": 1,
                "soc-mean": 0.68,
                "soc-std": 0.3,
                "proportion": 0.09,
            },
            # TODO: deal with this case
            # "Always plugged": {
            #     "pi-mean": 0,
            #     "pi-std": 0,
            #     "po-mean": 0,
            #     "po-std": 0,
            #     "soc-mean": 0.68,
            #     "soc-std": 0.3,
            #     "proportion": 0.01,
            # },
        }

        domain = (0, 24)
        plug_in_times = []
        plug_in_times_group = {}
        group_labels = []
        for group in USER_GROUPS:
            ave_samples = []
            for _ in range(no_of_iterations):
                samples = run_monte_carlo(
                    no_of_users=int(no_of_users * USER_GROUPS[group]["proportion"]),
                    mean_of_dist=USER_GROUPS[group]["pi-mean"],
                    std_of_dist=USER_GROUPS[group]["pi-std"],
                    repeatable=repeatable,
                    domain=domain,
                )
                plug_in_times.append(samples)
                group_labels.append(group)
                ave_samples.append(samples)
            plug_in_times_group[group] = np.mean(ave_samples, axis=0)

        metric = "EV plug-in time"
        fig_pi = distributions(
            plug_in_times,
            group_labels,
            metric,
            domain,
            show_hist=True,
            show_curve=False,
        )

        plug_out_times = []
        plug_out_times_group = {}
        group_labels = []
        for group in USER_GROUPS:
            ave_samples = []
            for _ in range(no_of_iterations):
                samples = run_monte_carlo(
                    no_of_users=int(no_of_users * USER_GROUPS[group]["proportion"]),
                    mean_of_dist=USER_GROUPS[group]["po-mean"],
                    std_of_dist=USER_GROUPS[group]["po-std"],
                    repeatable=repeatable,
                    domain=domain,
                )
                plug_out_times.append(samples)
                group_labels.append(group)
                ave_samples.append(samples)
            plug_out_times_group[group] = np.mean(ave_samples, axis=0)

        metric = "EV plug-out time"
        fig_po = distributions(
            plug_out_times,
            group_labels,
            metric,
            domain,
            show_hist=True,
            show_curve=False,
        )

        domain = (0, 1)
        plug_in_soc = []
        plug_in_soc_group = {}
        group_labels = []
        for group in USER_GROUPS:
            ave_samples = []
            for _ in range(no_of_iterations):
                samples = run_monte_carlo(
                    no_of_users=int(no_of_users * USER_GROUPS[group]["proportion"]),
                    mean_of_dist=USER_GROUPS[group]["soc-mean"],
                    std_of_dist=USER_GROUPS[group]["soc-std"],
                    repeatable=repeatable,
                    domain=domain,
                )
                plug_in_soc.append(samples)
                group_labels.append(group)
                ave_samples.append(samples)
            plug_in_soc_group[group] = np.mean(ave_samples, axis=0)

        metric = "EV state of charge"
        fig_soc = distributions(
            plug_in_soc, group_labels, metric, domain, show_hist=False, show_curve=True
        )

        # count in bins of 1 hour the plug in times
        plug_in_times = []
        for group in USER_GROUPS:
            plug_in_times.extend(plug_in_times_group[group])
        s_plug_in = pd.Series(plug_in_times)
        s_plug_in_count = (
            s_plug_in.value_counts(bins=range(0, 25)).sort_index().cumsum()
        )

        # count in bins of 1 hour the plug out times
        plug_out_times = []
        for group in USER_GROUPS:
            plug_out_times.extend(plug_out_times_group[group])
        s_plug_out = pd.Series(plug_out_times)
        s_plug_out_count = (
            s_plug_out.value_counts(bins=range(0, 25)).sort_index().cumsum()
        )
        # in each bin, take the number plugged in minus the number plugged out
        s_plug_in_out_count = no_of_users - (s_plug_out_count - s_plug_in_count)

        fig_plug_in_out = aggregate(s_plug_in_out_count)

        return fig_pi, fig_po, fig_soc, fig_plug_in_out
