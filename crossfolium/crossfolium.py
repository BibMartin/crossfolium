# -*- coding: utf-8 -*-
"""
Crossfolium
-----------

"""
from jinja2 import Template
import json

from branca.element import Figure, JavascriptLink, CssLink, Div, MacroElement


class Crossfilter(Div):
    def __init__(self, data, **kwargs):
        """Create a Crossfilter

        Returns
        -------
        Folium Crossfilter Object

        """
        super(Crossfilter, self).__init__(**kwargs)
        self._name = 'Crossfilter'

        self.data = data

        crossfilter_def = MacroElement()
        crossfilter_def._template = Template(("""
            {% macro script(this, kwargs) %}
                var {{this._parent.get_name()}} = {};
                {{this._parent.get_name()}}.data = {{this._parent.data}};
                {{this._parent.get_name()}}.crossfilter = crossfilter({{this._parent.get_name()}}.data);
                {{this._parent.get_name()}}.allDim = {{this._parent.get_name()}}.crossfilter.dimension(
                    function(d) {return d;});
            {% endmacro %}
            """))  # noqa
        self.add_child(crossfilter_def)

        self._template = Template(u"""
            {% macro header(this, kwargs) %}
                <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                </style>
            {% endmacro %}
            {% macro html(this, kwargs) %}
                <div id="{{this.get_name()}}">
                    {{this.html.render(**kwargs)}}
                </div>
            {% endmacro %}
            {% macro script(this, kwargs) %}
               dc.renderAll();
            {% endmacro %}
        """)

    def render(self, **kwargs):
        super(Crossfilter, self).render(**kwargs)

        figure = self._parent.get_root()
        assert isinstance(figure, Figure), (
            "You cannot render this Element if it's not in a Figure.")

        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/dc/1.7.5/dc.css"),
            name='dcjs_css')
        figure.header.add_child(
            CssLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css"),
            name='leaflet_css')
        figure.header.add_child(
            CssLink("https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"),
            name='bootstrap_css')

        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"),
            name='d3js')
        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/crossfilter/1.3.12/crossfilter.min.js"),  # noqa
            name='crossfilterjs')
        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/dc/2.0.0-beta.20/dc.js"),
            name='dcjs')
        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"),
            name='leaflet')
        figure.header.add_child(
            JavascriptLink("https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"),  # noqa
            name='underscorejs')


class PieFilter(Div):
    def __init__(self, crossfilter, column, name="", width=150, height=150, inner_radius=20,
                 weight=None, order=None, colors=None, label=None, **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(PieFilter, self).__init__(width=width, height=height, **kwargs)
        self._name = 'PieFilter'

        self.crossfilter = crossfilter
        self.column = column
        self.name = name
        self.width = width
        self.height = height
        self.inner_radius = inner_radius
        self.order = order
        self.weight = weight
        self.colors = [x for x in colors] if colors else None
        self.label = label

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">{{this.html.render(**kwargs)}}</div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};

            {{this.get_name()}}.dimension = {{this.crossfilter.get_name()}}.crossfilter.dimension(
                function(d) {return d["{{this.column}}"];});
            document.getElementById("{{this.get_name()}}").innerHTML =
                '<h4>{{this.name}} <small><a id="{{this.get_name()}}-reset">reset</a></small></h4>'
                + '<div id="{{this.get_name()}}-chart" class="dc-chart"></div>';

            {{this.get_name()}}.chart = dc.pieChart('#{{this.get_name()}}-chart')
                .width({{this.width}})
                .height({{this.height}})
                .dimension({{this.get_name()}}.dimension)
                .group({{this.get_name()}}.dimension.group()
                    {% if this.weight %}.reduceSum(function(d) {return d["{{this.weight}}"];})
                    {% else %}.reduceCount(){% endif %}
                    )
                .innerRadius({{this.inner_radius}})
                {% if this.label %}.label({{this.label}}){% endif %}
                {% if this.colors %}.ordinalColors({{this.colors}}){% endif %}
                {% if this.order %}.ordering(function (d) {
                    var out = null;
                    var order={{this.order}};
                    for (var j=0;j<order.length;j++) {
                        if (order[j]==d.key) {out = 1+j;}
                        }
                    return out;}){% endif %};
            d3.selectAll('#{{this.get_name()}}-reset').on('click',function () {
                {{this.get_name()}}.chart.filterAll();
                dc.redrawAll();
                });
        {% endmacro %}
        """)  # noqa


class RowBarFilter(Div):
    """TODO docstring here
    Parameters
    ----------
    """
    def __init__(self, crossfilter, column, name="", width=150, height=150, inner_radius=20,
                 weight=None, order=None, elastic_x=True, colors=None, **kwargs):
        super(RowBarFilter, self).__init__(width=width, height=height, **kwargs)
        self._name = 'RowBarFilter'

        self.crossfilter = crossfilter
        self.column = column
        self.name = name
        self.width = width
        self.height = height
        self.inner_radius = inner_radius
        self.order = order
        self.weight = weight
        self.elastic_x = elastic_x
        self.colors = [x for x in colors] if colors else None

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">{{this.html.render(**kwargs)}}</div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};

            {{this.get_name()}}.dimension = {{this.crossfilter.get_name()}}.crossfilter.dimension(
                function(d) {return d["{{this.column}}"];});
            document.getElementById("{{this.get_name()}}").innerHTML =
                '<h4>{{this.name}} <small><a id="{{this.get_name()}}-reset">reset</a></small></h4>'
                + '<div id="{{this.get_name()}}-chart" class="dc-chart"></div>';

            {{this.get_name()}}.chart = dc.rowChart('#{{this.get_name()}}-chart')
                .width({{this.width}})
                .height({{this.height}})
                .dimension({{this.get_name()}}.dimension)
                .group({{this.get_name()}}.dimension.group()
                    {% if this.weight %}.reduceSum(function(d) {return d["{{this.weight}}"];})
                    {% else %}.reduceCount(){% endif %}
                    )
                .elasticX({{this.elastic_x.__str__().lower()}})
                {% if this.colors %}.ordinalColors({{this.colors}}){% endif %}
                {% if this.order %}.ordering(function (d) {
                    var out = null;
                    var order={{this.order}};
                    for (var j=0;j<order.length;j++) {
                        if (order[j]==d.key) {out = 1+j;}
                        }
                    return out;}){% endif %};
            d3.selectAll('#{{this.get_name()}}-reset').on('click',function () {
                {{this.get_name()}}.chart.filterAll();
                dc.redrawAll();
                });
        {% endmacro %}
        """)  # noqa


class BarFilter(Div):
    def __init__(self, crossfilter, column, width=150, height=150, bar_padding=0.1,
                 domain=None, groupby=None, xlabel="", ylabel="", margins=None,
                 weight=None, elastic_y=True, xticks=None, time_format=None, **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(BarFilter, self).__init__(**kwargs)
        self._name = 'BarFilter'

        self.crossfilter = crossfilter
        self.column = column
        self.width = width
        self.height = height
        self.bar_padding = bar_padding
        self.domain = json.dumps(domain)
        self.groupby = groupby
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.margins = json.dumps(margins)
        self.xticks = json.dumps(xticks)
        self.time_format = time_format
        self.weight = weight
        self.elastic_y = elastic_y

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">{{this.html.render(**kwargs)}}</div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {
                domain : {{this.domain}},
                groupby : {{this.groupby}},
                xAxisTickValues : {{this.xticks}},
                };
            {{this.get_name()}}.dimension = {{this.crossfilter.get_name()}}.crossfilter.dimension(
                function(d) {
                    return Math.floor(
                        (d["{{this.column}}"]-{{this.get_name()}}.domain[0])/{{this.get_name()}}.groupby)
                        +{{this.get_name()}}.domain[0]/{{this.get_name()}}.groupby;
                    });
            {{this.get_name()}}.ticks = [];
            for (var j=0; j<{{this.get_name()}}.xAxisTickValues.length; j++) {
                {{this.get_name()}}.ticks[j] = {{this.get_name()}}.xAxisTickValues[j]/{{this.get_name()}}.groupby;
                }

            dc.barChart("#{{this.get_name()}}")
                .width({{this.width}})
                .height({{this.height}})
                .dimension({{this.get_name()}}.dimension)
                .group({{this.get_name()}}.dimension.group()
                    {% if this.weight %}.reduceSum(function(d) {return d["{{this.weight}}"];})
                    {% else %}.reduceCount(){% endif %}
                    )
                .x(d3.scale.linear().domain([
                    {{this.get_name()}}.domain[0]/{{this.get_name()}}.groupby,
                    {{this.get_name()}}.domain[1]/{{this.get_name()}}.groupby,
                    ]))
                .elasticY({{this.elastic_y.__str__().lower()}})
                .centerBar(false)
                .barPadding({{this.bar_padding}})
                .xAxisLabel("{{this.xlabel}}")
                .yAxisLabel("{{this.ylabel}}")
                .margins({{this.margins}})
                .xAxis()
                  .tickValues({{this.get_name()}}.ticks)
                  .tickFormat(function(x){
                      {%if this.time_format %}
                      var dateformat = d3.time.format("{{this.time_format}}");
                      return dateformat(new Date(x*{{this.get_name()}}.groupby));
                      {% else %}
                      return x*{{this.get_name()}}.groupby;
                      {% endif %}
                      });
        {% endmacro %}
        """)  # noqa


class TableFilter(Div):
    def __init__(self, crossfilter, columns, size=10, sort_by=None, ascending=True, **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(TableFilter, self).__init__(**kwargs)
        self._name = 'TableFilter'

        self.crossfilter = crossfilter
        self.columns = columns
        self.sort_by = sort_by
        self.ascending = ascending
        self.size = size

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
        <table id="{{this.get_name()}}" class="{{this.class_}}">
            <thead>
                <tr class="header">
                {%for col in this.columns%}<th>{{col}}</th>{% endfor %}
                </tr>
            </thead>
        </table>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};
            {{this.get_name()}}.dataTable = dc.dataTable('#{{this.get_name()}}');
            {{this.get_name()}}.dataTable
                .dimension({{this.crossfilter.get_name()}}.allDim)
                .group(function (d) { return 'dc.js extra line'; })
                .size({{this.size}})
                .columns([
                  {% for col in this.columns %}
                  function (d) { return d["{{col}}"]; },
                  {% endfor %}
                  ])
                {%if this.sort_by %}.sortBy(dc.pluck('{this.sort_by}'))
                {%if this.ascending %}.order(d3.ascending){% else %}.order(d3.descending){% endif %}
                {% endif %}
                .on('renderlet', function (table) {
                    table.select('tr.dc-table-group').remove();
                    });
        {% endmacro %}
        """)


class CountFilter(Div):
    def __init__(self, crossfilter, html_template="{filter}/{total}", **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(CountFilter, self).__init__(**kwargs)
        self._name = 'CountFilter'

        self.crossfilter = crossfilter
        self.html_template = html_template

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">
                {{this.html_template.format(
                    filter='<span class="filter-count"></span>',
                    total='<span class="total-count"></span>'
                    )}}
            </div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};
            {{this.get_name()}}.dataCount = dc.dataCount("#{{this.get_name()}}")
                .dimension({{this.crossfilter.get_name()}}.crossfilter)
                .group({{this.crossfilter.get_name()}}.crossfilter.groupAll()
                );
        {% endmacro %}
        """)


class ResetFilter(Div):
    def __init__(self, html="Reset all", **kwargs):
        """TODO docstring here
        Parameters
        ----------
        """
        super(ResetFilter, self).__init__(**kwargs)
        self._name = 'ResetFilter'

        self.html = html

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <a id="{{this.get_name()}}" class="{{this.class_}} reset-filters">{{this.html}}</a>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            d3.selectAll('.reset-filters').on('click', function () {
                dc.filterAll();
                dc.renderAll();
                });
        {% endmacro %}
        """)


class GeoChoroplethFilter(Div):
    """TODO docstring here
    Parameters
    ----------
    """
    def __init__(self, crossfilter, column, geojson, key_on='feature.properties.name',
                 name="", width=150, height=150, inner_radius=20,
                 weight=None, order=None, elastic_x=True, projection=None,
                 colors=None, **kwargs):
        super(GeoChoroplethFilter, self).__init__(width=width, height=height, **kwargs)
        self._name = 'GeoChoroplethFilter'

        self.crossfilter = crossfilter
        self.column = column
        self.geojson = geojson
        self.key_on = key_on
        self.name = name
        self.width = width
        self.height = height
        self.projection = projection
        self.inner_radius = inner_radius
        self.order = order
        self.weight = weight
        self.elastic_x = elastic_x
        self.colors = colors if colors else None

        self._template = Template(u"""
        {% macro header(this, kwargs) %}
            <style> #{{this.get_name()}} {
                {% if this.position %}position : {{this.position}};{% endif %}
                {% if this.width %}width : {{this.width[0]}}{{this.width[1]}};{% endif %}
                {% if this.height %}height: {{this.height[0]}}{{this.height[1]}};{% endif %}
                {% if this.left %}left: {{this.left[0]}}{{this.left[1]}};{% endif %}
                {% if this.top %}top: {{this.top[0]}}{{this.top[1]}};{% endif %}
                }
            </style>
        {% endmacro %}
        {% macro html(this, kwargs) %}
            <div id="{{this.get_name()}}" class="{{this.class_}}">{{this.html.render(**kwargs)}}</div>
        {% endmacro %}
        {% macro script(this, kwargs) %}
            var {{this.get_name()}} = {};

            {{this.get_name()}}.geojson = {{this.geojson}};

            {{this.get_name()}}.dimension = {{this.crossfilter.get_name()}}.crossfilter.dimension(
                function(d) {return d["{{this.column}}"];});
            document.getElementById("{{this.get_name()}}").innerHTML =
                '<h4>{{this.name}} <small><a id="{{this.get_name()}}-reset">reset</a></small></h4>'
                + '<div id="{{this.get_name()}}-chart" class="dc-chart"></div>';

            {{this.get_name()}}.chart = dc.geoChoroplethChart('#{{this.get_name()}}-chart')
                .width({{this.width}})
                .height({{this.height}})
                .dimension({{this.get_name()}}.dimension)
                .group({{this.get_name()}}.dimension.group()
                    {% if this.weight %}.reduceSum(function(d) {return d["{{this.weight}}"];})
                    {% else %}.reduceCount(){% endif %}
                    )
                .overlayGeoJson({{this.get_name()}}.geojson.features, "state",
                    function (feature) {return {{this.key_on}};}
                    )
                {% if this.projection %}.projection({{this.projection}}){% endif %}
                {% if this.colors %}.colors({{this.colors}}){% endif %}
                {% if this.order %}.ordering(function (d) {
                    var out = null;
                    var order={{this.order}};
                    for (var j=0;j<order.length;j++) {
                        if (order[j]==d.key) {out = 1+j;}
                        }
                    return out;}){% endif %};
            d3.selectAll('#{{this.get_name()}}-reset').on('click',function () {
                {{this.get_name()}}.chart.filterAll();
                dc.redrawAll();
                });
        {% endmacro %}
        """)  # noqa
