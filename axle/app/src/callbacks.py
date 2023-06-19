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


def count_plugged_in_bins(
    plug_in_times_group: dict,
    plug_out_times_group: dict,
    plug_in_soc_group: dict,
    no_of_users: int,
    user_groups: dict,
) -> tuple:
    # count in bins of 1 hour the plug in times
    x_range = range(0, 25, 1)
    plug_in_times, plug_in_times_upper, plug_in_times_lower = [], [], []
    for group in user_groups.keys():
        plug_in_times.extend(plug_in_times_group[group]["mean"])
        plug_in_times_upper.extend(
            plug_in_times_group[group]["mean"] + plug_in_times_group[group]["std"]
        )
        plug_in_times_lower.extend(
            plug_in_times_group[group]["mean"] - plug_in_times_group[group]["std"]
        )
    s_plug_in_count = (
        pd.Series(plug_in_times).value_counts(bins=x_range).sort_index().cumsum()
    )
    s_plug_in_count_upper = (
        pd.Series(plug_in_times_upper).value_counts(bins=x_range).sort_index().cumsum()
    )
    s_plug_in_count_lower = (
        pd.Series(plug_in_times_lower).value_counts(bins=x_range).sort_index().cumsum()
    )

    # count in bins of 1 hour the plug out times
    plug_out_times, plug_out_times_upper, plug_out_times_lower = [], [], []
    for group in user_groups.keys():
        plug_out_times.extend(plug_out_times_group[group]["mean"])
        plug_out_times_upper.extend(
            plug_out_times_group[group]["mean"] + plug_out_times_group[group]["std"]
        )
        plug_out_times_lower.extend(
            plug_out_times_group[group]["mean"] - plug_out_times_group[group]["std"]
        )

    s_plug_out_count = (
        pd.Series(plug_out_times).value_counts(bins=x_range).sort_index().cumsum()
    )
    s_plug_out_count_upper = (
        pd.Series(plug_out_times_upper).value_counts(bins=x_range).sort_index().cumsum()
    )
    s_plug_out_count_lower = (
        pd.Series(plug_out_times_lower).value_counts(bins=x_range).sort_index().cumsum()
    )

    # in each bin, take the number plugged in minus the number plugged out
    s_plug_in_out_count = (
        no_of_users - (s_plug_out_count - s_plug_in_count)
    ) / no_of_users
    s_plug_in_out_count_upper = (
        no_of_users - (s_plug_out_count_upper - s_plug_in_count_lower)
    ) / no_of_users
    s_plug_in_out_count_lower = (
        no_of_users - (s_plug_out_count_lower - s_plug_in_count_upper)
    ) / no_of_users

    return (
        s_plug_in_out_count,
        s_plug_in_out_count_upper,
        s_plug_in_out_count_lower,
    )


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
                "charging_rate": 7 / 60,  # % per hour
                "color": "#003f5c",
            },
            "Intel Octopus": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.52,
                "soc-std": 0.3,
                "proportion": 0.3,
                "charging_rate": 7 / 72.5,  # % per hour
                "color": "#444e86",
            },
            "Infrequent C": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.18,
                "soc-std": 0.3,
                "proportion": 0.1,
                "charging_rate": 7 / 60,  # % per hour
                "color": "#955196",
            },
            "Infrequent D": {
                "pi-mean": 18,
                "pi-std": 2,
                "po-mean": 7,
                "po-std": 1,
                "soc-mean": 0.73,
                "soc-std": 0.3,
                "proportion": 0.1,
                "charging_rate": 7 / 60,  # % per hour
                "color": "#dd5182",
            },
            "Scheduled": {
                "pi-mean": 22,
                "pi-std": 1,
                "po-mean": 9,
                "po-std": 1,
                "soc-mean": 0.68,
                "soc-std": 0.3,
                "proportion": 0.09,
                "charging_rate": 7 / 60,  # % per hour
                "color": "#ff6e54",
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
            #     "charging_rate": 7 / 60,  # % per hour
            #     "color": "#ffa600",
            # },
        }

        # TODO: repeated code!

        domain = (0, 24)
        plug_in_times = []
        plug_in_times_group = {}
        group_labels = []
        for group, _ in USER_GROUPS.items():
            ave_samples = []
            plug_in_times_group[group] = {}
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
            # variance across the iterations
            plug_in_times_group[group]["mean"] = np.mean(ave_samples, axis=0)
            plug_in_times_group[group]["std"] = np.std(ave_samples, axis=0)

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
        for group, _ in USER_GROUPS.items():
            plug_out_times_group[group] = {}
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
            # variance across the iterations
            plug_out_times_group[group]["mean"] = np.mean(ave_samples, axis=0)
            plug_out_times_group[group]["std"] = np.std(ave_samples, axis=0)

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
        for group, _ in USER_GROUPS.items():
            plug_in_soc_group[group] = {}
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
            # variance across the iterations
            plug_in_soc_group[group]["mean"] = np.mean(ave_samples, axis=0)
            plug_in_soc_group[group]["std"] = np.std(ave_samples, axis=0)

        metric = "EV state of charge"
        fig_soc = distributions(
            plug_in_soc, group_labels, metric, domain, show_hist=False, show_curve=True
        )

        (
            s_plug_in_out_count,
            s_plug_in_out_count_upper,
            s_plug_in_out_count_lower,
        ) = count_plugged_in_bins(
            plug_in_times_group,
            plug_out_times_group,
            plug_in_soc_group,
            no_of_users,
            USER_GROUPS,
        )

        x_range = range(0, 25, 1)
        soc_bins = pd.DataFrame()
        for group, _ in USER_GROUPS.items():
            group_plug_in = (
                pd.Series(plug_in_times_group[group]["mean"])
                .value_counts(bins=x_range)
                .sort_index()
                .cumsum()
            )
            group_plug_out = (
                pd.Series(plug_out_times_group[group]["mean"])
                .value_counts(bins=x_range)
                .sort_index()
                .cumsum()
            )
            group_plug_in_out = no_of_users * USER_GROUPS[group]["proportion"] - (
                group_plug_out - group_plug_in
            )
            time_intervals = group_plug_in.index

            soc = plug_in_soc_group[group]["mean"].copy()
            soc_upper = (
                plug_in_soc_group[group]["mean"].copy()
                + plug_in_soc_group[group]["std"].copy()
            )
            soc_lower = (
                plug_in_soc_group[group]["mean"].copy()
                - plug_in_soc_group[group]["std"].copy()
            )
            charging_rate = USER_GROUPS[group]["charging_rate"]
            no_online = 0
            # reorder time_intervals to start from midday
            time_intervals_reordered = time_intervals[12:].append(time_intervals[:12])
            for time_interval in time_intervals_reordered:
                print(time_interval)
                no_online = int(group_plug_in_out[time_interval])
                # increase soc[:no_online] by charging_rate
                soc[:no_online] = soc[:no_online] + charging_rate
                soc[soc > 1] = 1
                soc_upper[:no_online] = soc_upper[:no_online] + charging_rate
                soc_upper[soc_upper > 1] = 1
                soc_lower[:no_online] = soc_lower[:no_online] + charging_rate
                soc_lower[soc_lower > 1] = 1
                soc_bins.loc[time_interval, f"{group}_mean"] = np.mean(soc)
                soc_bins.loc[time_interval, f"{group}_upper"] = np.mean(
                    soc_upper
                ) + np.std(soc_upper)
                soc_bins.loc[time_interval, f"{group}_lower"] = np.mean(
                    soc_lower
                ) - np.std(soc_lower)

        print(soc_bins)
        soc_bins = soc_bins.sort_index()
        fig_plug_in_out = aggregate(
            s_plug_in_out_count,
            s_plug_in_out_count_upper,
            s_plug_in_out_count_lower,
            soc_bins,
            USER_GROUPS,
        )
        return fig_pi, fig_po, fig_soc, fig_plug_in_out
