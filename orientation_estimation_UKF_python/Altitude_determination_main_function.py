# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import obseervation_data_state_model_generation
import class_unscented_kalman_filter
import ground_truth_data_generation
import UKF_estimation_loop
import plotting_UKFestimation_results

def angular_rate_calc(xp,dt):
    
    
    P = (np.multiply(xp[:,1],  xp[:,3]) - xp[:,0] * xp[:,2]) * (2 / dt)
    R = (xp[:,2] * xp[:,3] + xp[:,0] * xp[:,1]) * (2 / dt)
    Q = (1 - 2 * (xp[:,1] ** 2 + xp[:,2] ** 2)) * (1 / dt)
         
    return P,R,Q
"""
Created on Tue Jul 11 09:14:20 2023

@author: zchen
"""
if __name__ == '__main__':
    
    n = 4 #size of the state vector
    m = 4 #size of the output vector
    samples_n = 50 # number of data samples
    Q_var = 0.1    # process noise covariance
    R_var = 0.1    # observation noise covariance
    SNR = 4    # SNR in dB
    
    # initialization of software, data extraction and processing for euler angle rates
    

    datapath =  r'C:\Vibro dataset\field_test_2023_06_13\static_vibro_field_test_2023_06_13 (1).dat'  #experiment datapath
 
    
    raw_measurementdata = pd.read_table(datapath,skiprows = 6 ,nrows = 10000, delimiter='\t',encoding='latin-1',engine='python')

    #initial quarternion values
    x_0 = np.zeros((n, 1))
    x_0[0, 0] = 0
    x_0[1, 0] = 1
    x_0[2, 0] = 0
    x_0[3, 0] = 1
    #initial quarternion values
    x_00 = np.zeros((n, 1))
    x_00[0, 0] = 100
    x_00[1, 0] = 100
    x_00[2, 0] = 100
    x_00[3, 0] = 100

    
    
    # generate observation data and state data
    mngm = obseervation_data_state_model_generation.MNGM2(samples_n, x_0,raw_measurementdata)
    mngm.generate_data()
   
    # construct class of unscented kalman filter
    ukf = class_unscented_kalman_filter.UKF(n, m)

    #generated data:
    dataX = mngm.x
    
    dataY = mngm.y
    
    #calculate standard deviation of observation data
    
    signal_std = [np.sqrt(np.var(dataY[:, 0])),np.sqrt(np.var(dataY[:, 1])),np.sqrt(np.var(dataY[:, 2])),np.sqrt(np.var(dataY[:, 3]))]
    
    nosie_std = np.array(signal_std)/(10**(SNR/10))
 
    # number of esimation iteration
    size_n = dataX.shape[0]
    
   
    # generate ground truth quarternions
    quarternion_true1,quarternion_true2,quarternion_true3,quarternion_true4 = ground_truth_data_generation.ground_truth_quarternion_generation(size_n,dataX,raw_measurementdata,mngm)
    
        
        
    
   
    # reset and initialize UKF estimation process
    ukf.resetUKF(Q_var,  R_var, x_00,raw_measurementdata)

    timeUpdateInput = np.zeros((n, 1))
    measurementUpdateInput = np.zeros((m, 1))
    

    # UKF estimation loop
    dataY,est_state,est_pitch_arr,est_roll_arr,est_yaw_arr = UKF_estimation_loop.main_unscented_kalman_filter_estimation_loop(nosie_std,size_n, n,dataY,dataX,ukf,mngm)
    
    # convert quarternions to angular rate
    P,R,Q = angular_rate_calc(est_state,mngm.dt) 
    P_true,R_true,Q_true = angular_rate_calc(dataX,mngm.dt)
    # observation data
    P_obs,R_obs,Q_obs = angular_rate_calc(dataY,mngm.dt) 
   
    # plot estimation results
    
    plotting_UKFestimation_results.plot_angular_rate_estimation_comparison(P_obs,R_obs,Q_obs,mngm,samples_n, P_true,Q_true,R_true,P,R,Q )
    
    plotting_UKFestimation_results.plot_quarternion_estimation_results(dataX,est_state)    
    
    
    # plotting_UKFestimation_results. plot_Euler_angle_estimation_results(est_roll_arr,est_yaw_arr,est_pitch_arr)
    
    
    
    
