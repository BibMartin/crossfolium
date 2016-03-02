# -*- coding: utf-8 -*-

import branca
import folium
import crossfolium


def test_no_marker_function():
    f = branca.element.Figure()
    c = crossfolium.Crossfilter([{'lat': 0, 'lng': 0}]).add_to(f)
    m = folium.Map().add_to(c)
    crossfolium.FeatureGroupFilter(c).add_to(m)

    out = ''.join(f.render().split())
    tmp = ''.join("""
        .marker_function = function(d) {
            return L.marker([d.lat, d.lng]);}
        """.split())
    assert tmp in out


def test_marker_function():
    f = branca.element.Figure()
    c = crossfolium.Crossfilter([{'lat': 0, 'lng': 0}]).add_to(f)
    m = folium.Map().add_to(c)
    g = crossfolium.FeatureGroupFilter(c).add_to(m)
    crossfolium.marker_function.MarkerFunction(
        lat='Latitude',
        lng='Longitude',
        popup='Popup',
        ).add_to(g)

    out = ''.join(f.render().split())
    tmp = ''.join("""
        .marker_function = function (d) {
            return L.marker([d["Latitude"], d["Longitude"]])
                .bindPopup(d["Popup"]);
            }
        """.split())
    assert tmp in out


def test_circle_marker_function():
    f = branca.element.Figure()
    c = crossfolium.Crossfilter([{'lat': 0, 'lng': 0}]).add_to(f)
    m = folium.Map().add_to(c)
    g = crossfolium.FeatureGroupFilter(c).add_to(m)
    crossfolium.marker_function.CircleMarkerFunction(
        radius=50000,
        radius_meter=True,
        stroke=False,
        fillColor='red',
        ).add_to(g)
    crossfolium.marker_function.CircleMarkerFunction(
        radius=10,
        radius_meter=False,
        weight=1,
        fillColor='green',
        ).add_to(g)

    out = ''.join(f.render().split())
    tmp = ''.join("""
        .marker_function = function (d) {
            return L.circle([d["lat"], d["lng"]],50000,{
                "fillColor": "red",
                "stroke": false
                }).setRadius(50000);
            }
        """.split())
    assert tmp in out

    tmp = ''.join("""
        .marker_function = function (d) {
            return L.circleMarker([d["lat"], d["lng"]],{
                "fillColor": "green",
                "weight": 1
                }).setRadius(10);
            }
        """.split())
    assert tmp in out


def test_awesome_marker_function():
    f = branca.element.Figure()
    c = crossfolium.Crossfilter([{'lat': 0, 'lng': 0}]).add_to(f)
    m = folium.Map().add_to(c)
    g = crossfolium.FeatureGroupFilter(c).add_to(m)
    crossfolium.marker_function.AwesomeMarkerFunction(
        icon='feature.icon',
        marker_color='feature.color',
        prefix='fa',
        spin=True,
        ).add_to(g)

    out = ''.join(f.render().split())
    tmp = ''.join("""
        .marker_function = function (d) {
            var marker = L.marker([d["lat"], d["lng"]]);
            var icon = L.AwesomeMarkers.icon({
                icon : d["icon"],
                prefix : "fa",
                markerColor : d["color"],
                iconColor : "white",
                spin : true,
                extraClasses : "",
                });
                marker.setIcon(icon);
                return marker;
                };
        """.split())
    assert tmp in out
