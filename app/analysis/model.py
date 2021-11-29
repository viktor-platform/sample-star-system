"""Copyright (c) 2021 VIKTOR B.V.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

VIKTOR B.V. PROVIDES THIS SOFTWARE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from math import sqrt, pi, cos
from typing import Dict

import plotly.graph_objects as go
from viktor.core import UserException

from .constants import YEAR_IN_SECONDS, AU_IN_M, GRAVITATIONAL_CONSTANT


def calculate_planet_properties(
        mass_planet: float,
        mass_star: float,
        eccentricity: float,
        perihelion: float
    ) -> Dict[str, float]:  # in [AU] and [kg]
    """Calculates the planet's orbital properties and returns them in a dictionary"""

    if eccentricity == 0:
        raise UserException("the eccentricity can not be 1")

    p = perihelion * (1 + eccentricity)  # semi latus rectum in AU
    a = p / (1 - eccentricity ** 2)  # AU
    b = p / sqrt(1 - eccentricity ** 2)  # AU

    star_constant = GRAVITATIONAL_CONSTANT * (mass_star + mass_planet) / (4 * pi ** 2)  # m^3 / s^2
    t = sqrt((a * AU_IN_M) ** 3 / star_constant)  # s

    return {
        "semi-major": a,  # AU
        "semi-minor": b,  # AU
        "period": t / YEAR_IN_SECONDS,  # years
        "r_max": 2 * a - perihelion
    }


def plot_orbit(eccentricity: float, perihelion: float):
    """Plot the planet's orbit in a plotly figure based on the eccentricity and minimum radius (perihelion)"""
    thetas = range(360)
    radii = []
    for theta in thetas:
        r = perihelion * (1 + eccentricity) / (1 + eccentricity * cos(deg_to_radians(theta)))
        radii.append(r)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=radii,
        theta=list(thetas),
        mode='lines',
        name='orbit',
        line_color='peru'
    ))

    fig.update_layout(
        title='Orbit of planet',
        showlegend=False
    )
    return fig


def deg_to_radians(theta: float) -> float:
    """Converts an angle in degrees to an angle in radians.

    Useful for trigonometry operations (tan, sin and cos) that require radians rather than degrees.
    """
    return theta * 2 * pi / 360
