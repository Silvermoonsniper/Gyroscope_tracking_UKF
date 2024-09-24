# Introduction
This is a Python project which uses unscented kalman filter to estimate gyroscope data for orientation determination for highly nonlinear system dynamics. 

Author: Zhengyu Chen



The illustration of aircraft orientation and axes [1]
<p align="center">
  <img src="https://private-user-images.githubusercontent.com/89796179/289580994-bf70db4b-32c1-450c-8697-e71d240e00ff.PNG?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDIzMDgzNzAsIm5iZiI6MTcwMjMwODA3MCwicGF0aCI6Ii84OTc5NjE3OS8yODk1ODA5OTQtYmY3MGRiNGItMzJjMS00NTBjLTg2OTctZTcxZDI0MGUwMGZmLlBORz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMTElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjExVDE1MjExMFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWMyODk0NmU1ZWNlYWI3NWExNjM2MWYzNDRhZGE0ZDFkZWUyZmJmZWIyMDdiMzIwNTEzOTAwZmExNGIxMjRkMDImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.CggjlwbkhscXX-dNL2YYcmYGdVxl3F8DK7e_UW87_2w"
 " width="800" />
</p> 

Process model :
```
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
```
Observation model:
```
        self.yi[0] = 2*(xi[1]*xi[3] - xi[0]*xi[2]) 
        self.yi[1] = 2*(xi[2]*xi[3] + xi[0]*xi[1]) 
        self.yi[2] = xi[0]**2 + xi[1]**2 -xi[2]**2 -xi[3]**2 
        self.yi[3] = 2*(xi[1]*xi[2] + xi[0]*xi[3])
        self.yi = self.yi/np.linalg.norm(self.yi)
```

# Usage of Software.
The software is completely written in python. To use it, download whole project with command:
```
        git@github.com:Silvermoonsniper/Gyroscope_tracking_UKF.git
```
Open main function with name 'Altitude_determination_main_function.py' in your IDE (Spyder, Pycharm...). Select project folder and run the whole file.
Estimation results and error analysis is plotted then.

Simulation setup:

 SNR:   4dB,
 Initial estimate: [100,100,100,100]^T



<p align="center">
  <img src="https://user-images.githubusercontent.com/89796179/283138546-24f1cd7b-ea2b-4106-af47-a962cec3b503.png"
 " width="800" />
</p> 
<p align="center">
  <img src="https://user-images.githubusercontent.com/89796179/283138548-f2d998e3-bcec-4c34-9800-1ea4ff2488c4.png"
 " width="800" />
</p> 
<p align="center">
  <img src="https://user-images.githubusercontent.com/89796179/283456821-d1dfb502-0418-4d7f-b28f-0a3ee46a74f6.png"
 " width="800" />
</p> 

# References.
[1] H. G. de Marina, F. J. Pereda, J. M. Giron-Sierra and F. Espinosa, "UAV Attitude Estimation Using Unscented Kalman Filter and TRIAD," in IEEE Transactions on Industrial Electronics, vol. 59, no. 11, pp. 4465-4474, Nov. 2012, doi: 10.1109/TIE.2011.2163913.
