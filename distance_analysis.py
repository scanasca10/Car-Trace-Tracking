# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:32:13 2018

@author: canascasco
"""

def distance_analysis(path, non_zero_distance):    
    same_distance = []
    for element1 in non_zero_distance:
        for element2 in non_zero_distance:
            if path[element1]['Distance[Km]'].equals(path[element2]['Distance[Km]']):
                same_distance.append(element1)
    
    return {'same':same_distance}

                    