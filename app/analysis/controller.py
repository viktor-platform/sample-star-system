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
from io import StringIO
from typing import Tuple

from munch import Munch
from viktor.api_v1 import API
from viktor.core import ViktorController, UserException
from viktor.views import DataItem, DataGroup, Summary, WebAndDataView, WebAndDataResult

from .model import calculate_planet_properties, plot_orbit
from .parametrization import ExampleParametrisation


class ExampleController(ViktorController):
    
    """Controller class which acts as interface for the Analysis entity type.

    This Analysis entity-type has:
     - parent entity-type: System
     - sibling-entity-type(s): Planet
     - child entity-types: none
    """

    label = 'planet analysis'
    summary = Summary()
    parametrization = ExampleParametrisation(width=20)  # makes the parametrisation only fill 20% of the width

    @WebAndDataView('Resulting Orbit', duration_guess=1)
    def get_data_view(self, params: Munch, entity_id: int, **kwargs) -> WebAndDataResult:
        """Creates the output WebAndDataView that is visible in the Web UI."""

        if params.planet is None:
            raise UserException("Select a planet")

        planet = get_planet_params(params)
        star_name, star_mass = get_star_values(entity_id)
        properties = calculate_planet_properties(
                planet.mass,
                star_mass,
                params.eccentricity,
                params.perihelion
        )

        # create data group for visualisation
        main_data_group = DataGroup(
            DataItem("Star name", star_name),
            DataItem("Planet name", planet.planet_name),
            DataItem("Orbit Period", properties["period"], suffix="years", number_of_decimals=3),
            DataItem("Semi-major axis", properties["semi-major"], suffix="AU", number_of_decimals=3),
            DataItem("Semi-minor axis", properties["semi-minor"], suffix="AU", number_of_decimals=3),
            DataItem("Furthest point from star", properties["r_max"], suffix="AU", number_of_decimals=3)
        )

        # create plot
        fig = plot_orbit(params.eccentricity, params.perihelion)
        html_fig = StringIO(fig.to_html())

        return WebAndDataResult(html=html_fig, data=main_data_group)


def get_star_values(entity_id: int) -> Tuple[str, float]:
    """Get values from the parent entity (System) based on the entity_id of this entity"""
    analysis_entity = API().get_entity(entity_id)  # current entity
    project_entity = analysis_entity.parent()
    project_params = project_entity.last_saved_params
    return project_params.star_name, project_params.star_weight


def get_planet_params(params: Munch) -> Munch:
    """Get values from the Planet entity based on the selected planet in analysis."""
    selected_planet = params.planet  # selected Planet entity
    planet_params = selected_planet.last_saved_params
    return planet_params
