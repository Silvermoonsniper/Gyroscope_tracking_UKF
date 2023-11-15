# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:27:23 2023

@author: zchen
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_angular_rate_estimation_comparison(dataY,R_obs,Q_obs,mngm,samples_n, P_true,Q_true,R_true,P,R,Q ):
    
    time = np.arange(samples_n)*mngm.dt
    plt.figure(figsize = [14,12])
    plt.subplot(411)
    plt.plot(time[0::], dataY[0:samples_n], 'g', label='x_1 original')  # X from the orginal ungm
    plt.plot(time[0::], P_true[0:samples_n])
    plt.plot(time, P[0:samples_n])
    plt.title('The estimation of angular velocity of Gyroscope')
    plt.legend(['Observation','real','estimate'])
    plt.xlabel('time (s)')
    plt.ylabel('angular rate Roll (degreee/s)')
    plt.subplot(412)
    plt.plot(time[0::], Q_obs[0:samples_n], 'g', label='x_1 original') 
    plt.plot(time[0::], Q_true[0:samples_n])
    plt.plot(time, Q[0:samples_n])
    plt.legend(['Observation','real','estimate'])
    plt.xlabel('time (s)')
    plt.ylabel('angular rate Pitch (degreee/s)')
    plt.subplot(413)
    plt.plot(time[0::], R_obs[0:samples_n], 'g', label='x_1 original') 
    plt.plot(time[0::], R_true[0:samples_n])
    plt.plot(time, R[0:samples_n])
    plt.legend(['Observation','real','estimate'])
    plt.xlabel('time (s)')
    plt.ylabel('angular rate yaw')
    plt.subplot(414)
    plt.plot(time[1::], P_true[0:samples_n-1] - P[1:samples_n])
    plt.plot(time[1::], Q_true[0:samples_n-1] - Q[1:samples_n])
    plt.plot(time[1::], R_true[0:samples_n-1] - R[1:samples_n])
    plt.xlabel('time (s)')
    plt.ylabel('estimation error (degreee/s)')
    plt.legend(['e_p', 'e_q', 'e_r'])
    plt.tight_layout()
    

def  plot_quarternion_estimation_results(dataX,est_state):
    
    ######################################################################################################################################
    plt.figure(figsize = [14,12])
    plt.subplot(411)
    plt.plot(dataX[:, 0], 'g', label='x_1 original')  # X from the orginal ungm
    
    plt.plot(est_state[:, 0], 'r--', label='x_1 estimated') #estimated X
    plt.xlabel('time step')
    plt.ylabel('$q_0$')
    plt.legend(['real','estimate'])
    plt.title('The comparison between estimated $q_0$ and real $q_0$')
    
    ######################################################################################################################################
    plt.subplot(412)
    plt.plot(dataX[:, 1], 'g', label='x_1 original')  # X from the orginal ungm
    plt.plot(est_state[:, 1], 'r--', label='x_1 estimated') #estimated X
    plt.xlabel('time step')
    plt.ylabel('$q_1$')
    plt.legend(['real','estimate'])
    plt.title('The comparison between estimated $q_1$ and real $q_1$')
    
    ######################################################################################################################################
    
    plt.subplot(413)
    plt.plot(dataX[:, 2], 'g', label='x_1 original')  # X from the orginal ungm
    plt.plot(est_state[:, 2], 'r--', label='x_1 estimated') #estimated X
    plt.xlabel('time step')
    plt.ylabel('$q_2$')
    plt.legend(['real','estimate'])
    plt.title('The comparison between estimated $q_2$ and real $q_2$')
   
    ######################################################################################################################################
    
    plt.subplot(414)
    plt.plot(dataX[:, 3], 'g', label='x_1 original')  # X from the orginal ungm
    plt.plot(est_state[:, 3], 'r--', label='x_1 estimated') #estimated X
    plt.xlabel('time step')
    plt.ylabel('$q_3$')
    plt.legend(['real','estimate'])
    plt.title('The comparison between estimated $q_3$ and real $q_3$')
    plt.tight_layout()
    plt.show()

  

def plot_Euler_angle_estimation_results(est_roll_arr,est_yaw_arr,est_pitch_arr):  
    
    plt.figure()
    plt.plot(est_roll_arr)
    plt.plot(est_yaw_arr)
    plt.plot(est_pitch_arr)
    plt.show()     
    
    
def plot_observation_data(dataY):
     plt.figure()
     plt.plot(dataY[:, 0], 'g', label='x_1 original')  # X from the orginal ungm
     plt.plot(dataY[:, 1], 'r', label='x_1 original')  # X from the orginal ungm    
     plt.plot(dataY[:, 2], 'b', label='x_1 original')  # X from the orginal ungm
     plt.plot(dataY[:, 3], 'c', label='x_1 original')  # X from the orginal ungm    
    