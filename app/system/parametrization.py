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
from viktor.parametrization import Parametrization, TextField, NumberField

_default_content = [
    {'planet_name': 'Earth', 'period': 1, 'eccentricity': 0.017},
    {'planet_name': 'Mars', 'period': 1.88, 'eccentricity': 0.093},
    {'planet_name': 'Saturn', 'period': 29.42, 'eccentricity': 0.054},
]


class SystemParametrisation(Parametrization):
    """Defines the input fields in left-side of the web UI in the System entity (Editor)."""
    star_name = TextField('Name', default="the Sun")
    star_weight = NumberField('Weight', default=1.9885e30, suffix='kg')
