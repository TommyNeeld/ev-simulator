from scipy.stats import norm
from numpy.random import RandomState
from scipy.stats.sampling import NumericalInversePolynomial


def run_monte_carlo(
    no_of_users: int, mean_of_dist=18, std_of_dist=2, repeatable=True, domain=(0, 24)
):
    """Run Monte Carlo simulation to generate random EV plug-in time."""
    extended_domain = (0, 34)
    if repeatable:
        random_state = RandomState(42)
    else:
        random_state = RandomState()

    # assume normal distribution
    normal_dist = norm(mean_of_dist, std_of_dist)

    # using NumericalInversePolynomial to generate inverse cdf with bounds

    # TODO: there must be a better way of handling 24 hour clock
    # if domain is (0, 24), extend bounds and remap
    if domain == (0, 24):
        domain = extended_domain
    inverse_cdf = NumericalInversePolynomial(normal_dist, domain=domain)
    inverse_cdf_samples = inverse_cdf.rvs(size=no_of_users, random_state=random_state)

    # if domain is (0, 24), remap to (0, 24)
    if domain == extended_domain:
        # anything greater than 24 is remapped to the morning
        inverse_cdf_samples[inverse_cdf_samples > 24] = (
            inverse_cdf_samples[inverse_cdf_samples > 24] - 24
        )

    return inverse_cdf_samples
