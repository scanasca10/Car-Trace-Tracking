# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:35:40 2018

@author: canascasco
"""
def get_unique(lista):
    output = set()
    for x in lista:
        output.add(x)
    
    return list(output)
