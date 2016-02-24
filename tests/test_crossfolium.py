# -*- coding: utf-8 -*-
""""
CrossFolium Test Module
-----------------------
"""
import crossfolium as cf


def test_true():
    c = cf.Crossfilter([])
    c._repr_html_()
