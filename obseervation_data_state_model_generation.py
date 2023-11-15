# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:09:04 2023

@author: zchen
"""

import numpy as np
from scipy.linalg import expm

class MNGM2:
    # class used for generation of nonlinear state  and corresponding observation
    def __init__(self, n, x_0,raw_measurementdata):

        self.n = n
        self.x = np.zeros((n, 4))
        self.y = np.zeros((n, 4))

        self.xi = np.zeros(4)
        self.yi = np.zeros(4)
        
        # sampling interval (s)
        self.dt = 1 
        self.angular_velocity = [0,0,0]
        # initialize for angular velocity
        self.P,self.Q,self.R  = 0.0023859*np.array(raw_measurementdata['gyro_x'])+ 0.11849,0.0095514*np.array(raw_measurementdata['gyro_y'])+ 0.073922,0.0093855*np.array(raw_measurementdata['gyro_z'])+ 0.52678
        # initialize state estimate of quarternion 
        self.x[0, :] = x_0[:, 0]
        
        self.u = np.random.normal(0., 0.1, 1)
        # initial bias for gyroscope
        self.b_0 = 0.2
        # noisy bias
        self.b = self.b_0 +np.random.normal(0., 0.1, (4, n))
        
        # initialize observed quarternion
        self.q_o = np.zeros(4)
        self.angular_velocity_measure = [0,0,0]
        #initial roll pitch and yaw angle
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        

    
    
    def angular_velocity_to_quaternion(self,angular_velocity, dt):
    # Normalize angular velocity
        norm = np.linalg.norm(angular_velocity)
        normalized_angular_velocity = angular_velocity / norm
        
    # Construct the skew-symmetric matrix
        skew_symmetric_matrix = np.array([
        [0, -normalized_angular_velocity[2], normalized_angular_velocity[1]],
        [normalized_angular_velocity[2], 0, -normalized_angular_velocity[0]],
        [-normalized_angular_velocity[1], normalized_angular_velocity[0], 0]
    ])

    # Compute the rotation matrix
        rotation_matrix = expm(skew_symmetric_matrix * dt)

    # Convert rotation matrix to quaternion
        self.quaternion = np.array([
        np.sqrt(1 + rotation_matrix[0, 0] + rotation_matrix[1, 1] + rotation_matrix[2, 2]) / 2,
        (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / (4 * np.sqrt(1 + rotation_matrix[0, 0] + rotation_matrix[1, 1] + rotation_matrix[2, 2])),
        (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / (4 * np.sqrt(1 + rotation_matrix[0, 0] + rotation_matrix[1, 1] + rotation_matrix[2, 2])),
        (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / (4 * np.sqrt(1 + rotation_matrix[0, 0] + rotation_matrix[1, 1] + rotation_matrix[2, 2]))
    ])

        return self.quaternion
    
    #  function to generate observation and state data
      
    def generate_data(self):
        
        for i in range(1, self.n):
            self.x[i, :] = self.state(i, self.x[i-1, :]) 
            
            self.y[i, :] = self.output(self.x[i, :],i) 

  
    def state(self, i, xp):

   
 
        
        # Compute angular velocity components#

        self.P[i] = (xp[1] * xp[3] - xp[0] * xp[2]) * (2 / self.dt)
        self.R[i] = (xp[2] * xp[3] + xp[0] * xp[1]) * (2 / self.dt)
        self.Q[i] = (1 - 2 * (xp[1] ** 2 + xp[2] ** 2)) * (1 / self.dt)

    
    #construct omega matrix
        self.omega_matrix = np.array([[0, -self.P[i], -self.Q[i], -self.R[i]],
                             [self.P[i],  0,  self.R[i], -self.Q[i]],
                             [self.Q[i], -self.R[i], 0,  self.P[i]],
                             [self.R[i], self.Q[i], -self.P[i],  0]])
        self.delta_w = 0.5* np.sqrt((self.P[i]*self.dt)**2 + (self.Q[i]*self.dt)**2 + (self.R[i]*self.dt)**2)
        
    # identity matrix
        self.I = np.eye(len(self.omega_matrix))
       
    #propagate for next state with discrete state space equation
    
        self.F_matrix = (self.I*np.cos(0.5*self.delta_w) + (np.sin(0.5*self.delta_w)*(0.5*self.delta_w)*self.omega_matrix))
        # convert measured angular velocity into quarternion
        self.angular_velocity = [self.P[i],self.Q[i],self.R[i]]
        xp = self.angular_velocity_to_quaternion(self.angular_velocity, self.dt)
        
        self.xi = np.matmul(self.F_matrix,xp) +np.random.normal(0., 4e-6, 4)
        # normalize quarternion
        
        self.xi = self.xi/np.linalg.norm(self.xi) 
       
        return self.xi

    # observation model, to determine roll, pitch and yaw angle
    # input args:
        
    #      xi: state variable
   # output args:
    #       self.yi: observation vector with following explation:
    #           self.yi[0]:
    #           self.yi[1]:
    #           self.yi[2]:
    #           self.yi[3]:
               
    def output(self, xi,i):
        
    
        
        
        self.yi[0] = 2*(xi[1]*xi[3] - xi[0]*xi[2]) 
        self.yi[1] = 2*(xi[2]*xi[3] + xi[0]*xi[1]) 
        self.yi[2] = xi[0]**2 + xi[1]**2 -xi[2]**2 -xi[3]**2 
        self.yi[3] = 2*(xi[1]*xi[2] + xi[0]*xi[3])
        self.yi = self.yi/np.linalg.norm(self.yi)
        return self.yi
    # function to calculate euelr angles from quarternions 
    def quaternion_to_euler(self,xi):
        
        
    # Roll (X-axis rotation)
        self.roll = np.arctan2(2*(xi[0]*xi[1] + xi[2]*xi[3]), 1 - 2*(xi[1]**2 + xi[2]**2))
    # Pitch (Y-axis rotation)
        self.pitch = np.arcsin(2*(xi[0]*xi[2] - xi[3]*xi[1]))
    # Yaw (Z-axis rotation)
        self.yaw = np.arctan2(2*(xi[0]*xi[3] + xi[1]*xi[2]), 1 - 2*(xi[2]**2 + xi[3]**2))
        return self.roll, self.pitch, self.yaw