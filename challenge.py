# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:35:19 2018

@author: canascasco
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from path_analysis import path_analysis
from speed_analysis import speed_analysis
from speed_analysis2 import speed_analysis2
from rute_analysis import rute_analysis
from get_unique import get_unique
from distance_analysis import distance_analysis
from trace_analysis import trace_analysis



flag = input('small data set [1]/ large data set[0]: ') 
    
if flag == '0': 
    file = 'Tracebox_subset_8917chains_large.csv'
else:
    file = 'Tracebox_subset_81chains_small.csv'

df = pd.read_csv(file)
chunksize =  2*10**3

users, path = {},{}
walking_users, driving_users, other_users, same_distance, same_ending, same_position, same_starting = [],[],[],[],[],[],[]
TMSI = input('Enter your TMSI: ') 

for chunk in pd.read_csv(file,chunksize = chunksize):          
    tmsi = list(chunk['M_TMSI'])      
    subscriber = [] # list of all the subscribers based on their M_TMSI
    for e in tmsi:
        if e not in subscriber:
            subscriber.append(e)
        
    indexes = []
    for element in subscriber :
        indexes.append(tmsi.index(element))
            
    indexes.append(len(tmsi)) # Add the last index
            
    df_user = {} # It is a dictionary, each TMSI is the key, and the value is a data frame
    for i in range(0, len (subscriber)) :
        df_user[subscriber[i]] = chunk[indexes[i]:indexes[i+1]]  
                      
    trace = trace_analysis(df_user, subscriber)
    trace_keys = trace_analysis(df_user, subscriber).keys()
        
    '''
    filtering data based on big changes in position, the speed of those changes are calculated 
     '''
    for element in trace_keys:
        delta, dist, speed = [],[],[]
        for i in range( 0, len(trace[element]['time[h]']) ):
            delta.append( abs(datetime.strptime( trace[element]['time[h]'][i][0], '%Y-%m-%d %H:%M:%S' ) 
            - datetime.strptime(trace[element]['time[h]'][i][1], '%Y-%m-%d %H:%M:%S') ).total_seconds()/(3600))  # Time expressed in hours
            dist.append(trace[element]['distance[Km]'])
            if delta[i] == 0:
                continue
            speed.append(dist[0][i]/delta[i])
        trace[element]['Speed[Km/h]'] = speed
        
    '''
    filtering data based on their path (origin/ destination)
    '''
    path.update(path_analysis(df_user, subscriber))
        
    '''
    filtering data based on their speed
    '''

    users.update(speed_analysis(trace))
    walking_users.append(get_unique(speed_analysis2(trace)['walking']))
    walking_ = get_unique(speed_analysis2(trace)['walking'])
    driving_users.append(get_unique(speed_analysis2(trace)['driving']))
    driving_ = get_unique(speed_analysis2(trace)['driving'])
    other_users.append(get_unique(speed_analysis2(trace)['other']))
    other_ = get_unique(speed_analysis2(trace)['other'])
        
    non_zero_distance = walking_ + driving_ + other_
        
    '''
    filtering data based on the initial/final position of the users
    '''
    same_starting.append(rute_analysis(path)['starting']) 
    same_ending.append(rute_analysis(path)['ending'] )
    same_position.append(rute_analysis(path)['same']) 
         
    '''
    filtering data based on the distance
    '''       
    same_distance.append(distance_analysis(path, non_zero_distance)['same'])            
    
    """
    Representation of the different traces of the subscribers
    """
    lat, lon, coordinate = [],[],[]
    if TMSI == '0':
        for element in non_zero_distance:
            lat = df_user[element]['POS_LAST_LAT'].T
            lon = df_user[element]['POS_LAST_LON'].T
            coordinate = list(zip(lat, lon))
            plt.plot(*zip(*coordinate), marker='o', color='r', ls='-')
            plt.xlim([48, 48.25])
            plt.xlabel('latitude')
            plt.ylim([11, 12])
            plt.ylabel('longitude')
            print('Subscriber: ', element)
            plt.show()
            continue
        
    
    else:
        if TMSI in non_zero_distance:
            lat = df_user[TMSI]['POS_LAST_LAT'].T
            lon = df_user[TMSI]['POS_LAST_LON'].T
            coordinate = list(zip(lat, lon))
            plt.plot(*zip(*coordinate), marker='o', color='b', ls='-')
            plt.xlim([48, 48.25])
            plt.xlabel('latitude')
            plt.ylim([11, 12])
            plt.ylabel('longitude')
            print(path[TMSI])
            plt.show()
            break



                
