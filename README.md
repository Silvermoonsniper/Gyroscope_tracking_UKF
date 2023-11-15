# Introduction
This is a Python project which uses unscented kalman filter to estimate gyroscope data for orientation determination for highly nonlinear system dynamics. 

Author: Zhengyu Chen

AG Marine Engineering Geology, MARUM, University of Bremen.

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
<p align="center">
  <img src="https://user-images.githubusercontent.com/89796179/283133756-649fbd79-20ca-44e4-9820-8e4da889da60.png"
 " width="400" />
</p> 
<p align="center">
  <img src="https://user-images.githubusercontent.com/89796179/283133763-06133a12-21b6-4bab-8f9a-bbbaeacd2b04.png"
 " width="400" />
</p> 

# References.
H. G. de Marina, F. J. Pereda, J. M. Giron-Sierra and F. Espinosa, "UAV Attitude Estimation Using Unscented Kalman Filter and TRIAD," in IEEE Transactions on Industrial Electronics, vol. 59, no. 11, pp. 4465-4474, Nov. 2012, doi: 10.1109/TIE.2011.2163913.
