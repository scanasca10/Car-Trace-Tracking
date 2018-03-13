# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 15:52:44 2018

@author: canascasco
"""

def  speed_analysis2 (path):
    users = {}
    walking_users, driving_users, other_users = [],[],[]
    for element in path:
        if not path[element]['Speed[Km/h]']:
            continue
        user = []    
        for i in range(0, len(path[element]['Speed[Km/h]'])):       
            if path[element]['Speed[Km/h]'][i] > 0.0 and path[element]['Speed[Km/h]'][i] <= 5.0:
                user.append({ 'Walking': path[element]['Speed[Km/h]'][i] })
                walking_users.append(element)
            elif path[element]['Speed[Km/h]'][i] > 5.0 and path[element]['Speed[Km/h]'][i] <= 50.0:
                user.append({ 'Driving':path[element]['Speed[Km/h]'][i] })
                driving_users.append(element)
            else:
                user.append({ 'Other': path[element]['Speed[Km/h]'][i] })
                other_users.append(element)
        
        users[element] = user[:]
        
    return {'walking':walking_users, 'driving': driving_users, 'other': other_users}
  