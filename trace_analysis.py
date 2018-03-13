# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:47:41 2018

@author: canascasco
"""
from distance import distance
def trace_analysis(df_user, subscriber):      
    trace= {} 
    for element in subscriber:
        current, previous, time, dist, speed = [],[],[],[],[]   
        speed = [0]*len(df_user[element])
        for i in range(1, len (df_user[element])):
            if distance([df_user[element]['POS_LAST_LAT'].iloc[i],
                         df_user[element]['POS_LAST_LON'].iloc[i]],
                        [df_user[element]['POS_LAST_LAT'].iloc[i-1],
                         df_user[element]['POS_LAST_LON'].iloc[i-1]]) > 1:
                
                
                current.append([df_user[element]['POS_LAST_LAT'].iloc[i], 
                                df_user[element]['POS_LAST_LON'].iloc[i]])
                
                previous.append([df_user[element]['POS_LAST_LAT'].iloc[i-1], 
                                df_user[element]['POS_LAST_LON'].iloc[i-1]])
                
                time.append([df_user[element]['END_TIME'].iloc[i],
                             df_user[element]['END_TIME'].iloc[i-1]])
                
                dist.append(distance([df_user[element]['POS_LAST_LAT'].iloc[i],
                         df_user[element]['POS_LAST_LON'].iloc[i]],
                        [df_user[element]['POS_LAST_LAT'].iloc[i-1],
                         df_user[element]['POS_LAST_LON'].iloc[i-1]]))
                
            trace[element] = {'current [lat/lon]': current,'previuos[lat/lon]': previous,
                 'time[h]': time, 'distance[Km]': dist, 'Speed[Km/h]': speed}
            
    return trace