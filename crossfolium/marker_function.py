# -*- coding: utf-8 -*-
"""
Marker Function
---------------

This defines objects that can be hooked to map.FeatureFilter to style the markers.
"""
from jinja2 import Template
import json

from branca.element import MacroElement


class MarkerFunction(MacroElement):
    """A simple marker with no flourish.

    Parameters
    ----------
    lat : str, default 'lat'
        The name of the latitude column in the data set.
    lng : str, default 'lng'
        The name of the longitude column in the data set.
    popup: str, default None
        The name of (eventual) popup string in the data set.
    """
    def __init__(self, lat='lat', lng='lng', popup=None):
        super(MarkerFunction, self).__init__()
        self._name = 'MarkerFunction'

        self.lat = lat
        self.lng = lng
        self.popup = popup

        self._template = Template(
            '{% macro script(this, kwargs) %}'
            '{{this._parent.get_name()}}.marker_function = function (d) {'
            'return L.marker([d["{{this.lat}}"], d["{{this.lng}}"]])'
            '{% if this.popup %}.bindPopup(d["{{this.popup}}"]){% endif %}'
            ';}'
            '{% endmacro %}'
            )


class CircleMarkerFunction(MacroElement):
    """A circleMarker with radius specified in pixels (or in meters).

    Parameters
    ----------
    lat : str, default 'lat'
        The name of the latitude column in the data set.
    lng : str, default 'lng'
        The name of the longitude column in the data set.
    popup: str, default None
        The name of (eventual) popup string in the data set.
    radius: int, default 10
        To specify the radius (in pixels) of cirlces.
    radius_meter: bool, default False
        If True, the radius is specified in meters so that the circles will
        grow when you zoom in.
        If False, the radius is in pixels.
    **kwargs:
        You can add eventually other arguments to style the markers.
        See `http://leafletjs.com/reference.html#path-options`.
    """
    def __init__(self, lat='lat', lng='lng', popup=None,
                 radius=None, radius_meter=False, **kwargs):
        super(CircleMarkerFunction, self).__init__()
        self._name = 'CircleMarkerFunction'

        self.lat = lat
        self.lng = lng
        self.popup = popup
        self.radius = radius
        self.radius_meter = radius_meter
        self.kwargs_str = json.dumps(kwargs, sort_keys=True)

        self._template = Template(
            '{% macro script(this, kwargs) %}'
            '{{this._parent.get_name()}}.marker_function = function (d) {return L.'
            '{% if this.radius_meter %}circle([d["{{this.lat}}"], d["{{this.lng}}"]],{{this.radius}}'  # noqa
            '{% else %}circleMarker([d["{{this.lat}}"], d["{{this.lng}}"]]'
            '{% endif %},{{this.kwargs_str}})'
            '{% if this.radius %}.setRadius({{this.radius}}){% endif %}'
            '{% if this.popup %}.bindPopup(d["{{this.popup}}"]){% endif %}'
            ';}'
            '{% endmacro %}'
            )


class AwesomeMarkerFunction(MacroElement):
    """A circleMarker with radius specified in pixels (or in meters).

    Parameters
    ----------
    lat : str, default 'lat'
        The name of the latitude column in the data set.
    lng : str, default 'lng'
        The name of the longitude column in the data set.
    popup: str, default None
        The name of (eventual) popup string in the data set.
    radius: int, default 10
        To specify the radius (in pixels) of cirlces.
    radius_meter: bool, default False
        If True, the radius is specified in meters so that the circles will
        grow when you zoom in.
        If False, the radius is in pixels.
    **kwargs:
        You can add eventually other arguments to style the markers.
        See `https://github.com/lvoogdt/Leaflet.awesome-markers`.
    """
    def __init__(self, lat='lat', lng='lng', popup=None,
                 icon='home', prefix='glyphicon', marker_color='blue',
                 icon_color='white', spin=False, extra_classes=""):
        super(AwesomeMarkerFunction, self).__init__()
        self._name = 'AwesomeMarkerFunction'

        self.lat = lat
        self.lng = lng
        self.popup = popup

        self.icon = icon
        self.prefix = prefix
        self.marker_color = marker_color
        self.icon_color = icon_color
        self.spin = spin
        self.extra_classes = extra_classes

        self._template = Template(
            '{% macro script(this, kwargs) %}'
            '{{this._parent.get_name()}}.marker_function = function (d) {'
            '    var marker = L.marker([d["{{this.lat}}"], d["{{this.lng}}"]])'
            '        {% if this.popup %}.bindPopup(d["{{this.popup}}"]){% endif %}'
            '    ;'
            '    var icon = L.AwesomeMarkers.icon({'
            '        icon : {% if this.icon.startswith("feature.") %}d["{{this.icon[8:]}}"]'
            '            {% else %}"{{this.icon}}"{% endif %},'
            '        prefix : {% if this.prefix.startswith("feature.") %}d["{{this.prefix[8:]}}"]'
            '            {% else %}"{{this.prefix}}"{% endif %},'
            '        markerColor : {% if this.marker_color.startswith("feature.") %}d["{{this.marker_color[8:]}}"]'  # noqa
            '            {% else %}"{{this.marker_color}}"{% endif %},'
            '        iconColor : {% if this.icon_color.startswith("feature.") %}d["{{this.icon_color[8:]}}"]'  # noqa
            '            {% else %}"{{this.icon_color}}"{% endif %},'
            '        spin : {% if this.spin.__str__().startswith("feature.") %}d["{{this.spin[8:]}}"]'  # noqa
            '            {% else %}{{this.spin.__str__().lower()}}{% endif %},'
            '        extraClasses : {% if this.extra_classes.startswith("feature.") %}d["{{this.extra_classes[8:]}}"]'  # noqa
            '            {% else %}"{{this.extra_classes}}"{% endif %},'
            '        });'
            '    marker.setIcon(icon);'
            '    return marker;'
            '    };'
            '{% endmacro %}'
            )  # noqa
