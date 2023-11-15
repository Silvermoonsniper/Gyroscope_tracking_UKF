# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:39:16 2023

@author: zchen
"""

import numpy as np


def main_unscented_kalman_filter_estimation_loop(signal_std,size_n, n,dataY,dataX,ukf,mngm):
    
    err_total = 0

    est_state = np.zeros((size_n, n))
    est_output = np.zeros((size_n, n))
    
    # estimate quarternion
    estimate_quarternion = np.zeros(4)
    
    # estimate roll, pitch yaw angle array
    est_roll_arr = []
    est_pitch_arr = []
    est_yaw_arr = []
    # add AWGN to observation data
    dataY[:, 0] = dataY[:, 0] + np.random.normal(0., signal_std[0], len(dataY[:, 0]))
    dataY[:, 1] = dataY[:, 1] + np.random.normal(0., signal_std[1], len(dataY[:, 0]))
    dataY[:, 2] = dataY[:, 2] + np.random.normal(0., signal_std[2], len(dataY[:, 0]))
    dataY[:, 3] = dataY[:, 3] + np.random.normal(0., signal_std[3], len(dataY[:, 0]))
    print(signal_std[0])
    # estimation loop
    for i in range(size_n):

        timeUpdateInput = i
        measurementUpdateInput = dataY[i, :]  
      
        # recursively go through time update and measurement correction
        ukf.timeUpdate(timeUpdateInput)
        ukf.measurementUpdate(measurementUpdateInput)

        err = 0
        for j in range(n):
            err = err + (ukf.x_aposteriori[j] - dataX[i, j])**2

        est_state[i, 0] = ukf.x_aposteriori[0]
        est_state[i, 1] = ukf.x_aposteriori[1]
        est_state[i, 2] = ukf.x_aposteriori[2]
        est_state[i, 3] = ukf.x_aposteriori[3]
        
        
        est_output[i, 0] = ukf.y[0]
        est_output[i, 1] = ukf.y[1]
        est_output[i, 2] = ukf.y[2]
        est_output[i, 3] = ukf.y[3]
        est_output[i, 0] = ukf.K[0, 1]

        err_total = err_total + err
        
        estimate_quarternion = [est_state[i, 0],est_state[i, 1],est_state[i, 2],est_state[i, 3]]
        
        roll, pitch, yaw  = mngm.quaternion_to_euler(estimate_quarternion)
        
        est_roll_arr.append(roll)
        est_pitch_arr.append(pitch)
        est_yaw_arr.append(yaw)
    
    return dataY,est_state,est_pitch_arr,est_roll_arr,est_yaw_arr