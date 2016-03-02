# -*- coding: utf-8 -*-
"""
Map
---

All the part of crossfolium that is about drawing things in a folium.Map.
"""
from jinja2 import Template

from folium.map import FeatureGroup
from folium.plugins import HeatMap


class FeatureGroupFilter(FeatureGroup):
    def __init__(self, crossfilter, name=None, fit_bounds=False,
                 circle_radius=None, color="#0000ff", opacity=1., **kwargs):
        """
        """
        super(FeatureGroupFilter, self).__init__(**kwargs)
        self._name = 'FeatureGroupFilter'

        self.tile_name = name if name is not None else self.get_name()

        self.crossfilter = crossfilter
        self.fit_bounds = fit_bounds
        self.circle_radius = circle_radius
        self.color = color
        self.opacity = opacity

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};
            {{this.get_name()}}.feature_group = new L.FeatureGroup();
            {{this.get_name()}}.marker_function = function(d) {return L.marker([d.lat, d.lng]);}
            {{this.get_name()}}.updateFun = function() {
                this.feature_group.clearLayers();
                var dimVals = {{this.crossfilter.get_name()}}.allDim.top(Infinity)
                for (var i in dimVals) {
                var d = dimVals[i];
                    var marker = this.marker_function(d);
                    this.feature_group.addLayer(marker);
                    }
                {{this._parent.get_name()}}.addLayer(this.feature_group);
                {% if this.fit_bounds %}{{this._parent.get_name()}}
                    .fitBounds(this.feature_group.getBounds());{% endif %}
                }
            dc.dataTable('#foo')
               .dimension({{this.crossfilter.get_name()}}.allDim)
               .group(function (d) { return 'dc.js';})
               .on('renderlet', function (table) { {{this.get_name()}}.updateFun();});
            {{this.get_name()}}.updateFun();
        {% endmacro %}
        """)


class HeatmapFilter(HeatMap):
    def __init__(self, crossfilter, name=None, fit_bounds=False, **kwargs):
        """
        """
        super(HeatmapFilter, self).__init__([], **kwargs)
        self._name = 'HeatmapFilter'

        self.crossfilter = crossfilter
        self.fit_bounds = fit_bounds

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};
            {{this.get_name()}}.heatmap = new L.heatLayer(
                {},
                {
                    minOpacity: {{this.min_opacity}},
                    maxZoom: {{this.max_zoom}},
                    max: {{this.max_val}},
                    radius: {{this.radius}},
                    blur: {{this.blur}},
                    gradient: {{this.gradient}}
                    })
                .addTo({{this._parent.get_name()}});
            {{this.get_name()}}.updateFun = function() {
                // this.heatmap.clearLayers();
                var dimVals = {{this.crossfilter.get_name()}}.allDim.top(Infinity);
                var latlngs = [];
                for (var i in dimVals) {
                    var d = dimVals[i];
                    latlngs.push([d.lat, d.lng]);
                    }
                {{this.get_name()}}.heatmap.setLatLngs(latlngs);
                {% if this.fit_bounds %}{{this._parent.get_name()}}
                    .fitBounds(this.heatmap.getBounds());{% endif %}
                }
            dc.dataTable('#foo')
               .dimension({{this.crossfilter.get_name()}}.allDim)
               .group(function (d) { return 'dc.js';})
               .on('renderlet', function (table) { {{this.get_name()}}.updateFun();});
            {{this.get_name()}}.updateFun();
        {% endmacro %}
        """)
