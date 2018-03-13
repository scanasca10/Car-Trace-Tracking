# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:35:23 2018

@author: canascasco
"""

from math import sin, cos, sqrt, atan2, radians
def distance( pos1, pos2):
    R = 6373.0
    lat1 = radians(pos1[0]) 
    lon1 = radians(pos1[1])
    lat2 = radians(pos2[0])
    lon2 = radians(pos2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
