# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:23:33 2018

@author: User
"""
from distance import distance
import pandas as pd
from datetime import datetime
def path_analysis(df_user, subscriber):      
    origin_, destination_, tdelta, speed = [],[],[],[]
    path = {}
    for element in subscriber: 
        tdelta = (datetime.strptime(df_user[element]['END_TIME'].iloc[-1], '%Y-%m-%d %H:%M:%S') 
                  - datetime.strptime(df_user[element]['END_TIME'].iloc[0], '%Y-%m-%d %H:%M:%S')).total_seconds()/(3600)  # Time expressed in hours
        
        origin_ = (df_user[element]['POS_LAST_LAT'].iloc[0], 
                   df_user[element]['POS_LAST_LON'].iloc[0])  # (origin_lat, origin_lon)
        
        destination_ = (df_user[element]['POS_LAST_LAT'].iloc[-1],
                        df_user[element]['POS_LAST_LON'].iloc[-1]) #(destination_lat, destination_lon)
        
        if tdelta == 0:
            tdelta = 1
        
        speed = abs(distance(origin_, destination_)/tdelta)      
        path[element] = pd.DataFrame( data = {'Origin' : origin_, 'Destination' : destination_, 
            'Distance[Km]' : abs(distance(origin_, destination_)), 'Time[h]' : abs(tdelta) ,
            'Speed[Km/h]' : speed} ) # It includes the 'speed' of the subscribers  
    return path