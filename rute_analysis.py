# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:17:55 2018

@author: canascasco
"""
def rute_analysis (path):
    same_starting, same_ending, same_ = [],[],[]
    for element1 in path:
        for element2 in path:
            if path[element1]['Origin'].equals(path[element2]['Origin']):
                same_starting.append(element1)
            if path[element1]['Destination'].equals(path[element2]['Destination']): 
                same_ending.append(element1)
            if path[element1]['Origin'].equals(path[element2]['Origin']) and path[element1]['Destination'].equals(path[element2]['Destination']):   
               same_.append(element1)
               
    return {'starting':same_starting, 'ending':same_ending, 'same': same_}
