# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:32:20 2023

@author: zchen
"""
import numpy as np



def ground_truth_quarternion_generation(size_n,dataX,raw_measurementdata,mngm):
    
    
    quarternion_true1 = []
    quarternion_true2 = []
    quarternion_true3 = []
    quarternion_true4 = []
      
        
 
    for i in range(size_n):
        true_gyro_x = 0.0023859*np.array(raw_measurementdata['gyro_x'])[i]+ 0.11849
        true_gyro_y = 0.0095514*np.array(raw_measurementdata['gyro_y'])[i]+ 0.073922
        true_gyro_z = 0.0093855*np.array(raw_measurementdata['gyro_z'])[i]+ 0.52678
        angular_velocity_measuretrue = [true_gyro_x,true_gyro_z,true_gyro_y]
        quarternion_true = mngm.angular_velocity_to_quaternion(angular_velocity_measuretrue, 0.001)
        
        quarternion_true1.append(quarternion_true[0])
        quarternion_true2.append(quarternion_true[1])
        quarternion_true3.append(quarternion_true[2])
        quarternion_true4.append(quarternion_true[3])
        
    return quarternion_true1,quarternion_true2,quarternion_true3,quarternion_true4