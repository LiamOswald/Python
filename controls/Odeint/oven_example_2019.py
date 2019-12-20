import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

wait = 0
Qdot = 0

# Tddot = -tau * (T-T_inf) + Qdot

def Derivatives(z,t):
    global wait,Qdot
    Tdot = z[1]
    T = z[0]
    temp_error_integral = z[2]
    zeta = 1
    wn = 0.1
    T_inf = 72 
    T_bake = 350
    ##Bang bang control
    threshold = 10
    if wait == 0:
        if T < (T_bake+threshold):
            Qdot = 400 
        else:
            wait = 1
            Qdot = 0
    else:
        if T < (T_bake-threshold):
            wait = 0
            Qdot = 400
        else:
            Qdot = 0
    ##Proportional Control
    #kp = -10
    #ki = -0.1
    temp_error = T-T_bake
    temp_error_integral_derivative = temp_error
    
    #Qdot = kp*temp_error + ki*temp_error_integral
    #if Qdot > 400:
    #    Qdot = 400
    #if Qdot < 0:
    #    Qdot = 0
    
    Tddot = -wn**2 * (T-T_inf) - 2*zeta*wn*Tdot + wn**2*Qdot
    zdot = np.asarray([Tdot,Tddot,temp_error_integral_derivative])
    return zdot

plt.close("all")

tout = np.linspace(0,100,1000)
timestep = tout[1]-tout[0]
zinitial = np.asarray([72,0,0])
zout = S.odeint(Derivatives,zinitial,tout)

plt.plot(tout,zout[:,0])

plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (F)')

##I'd also like to plot control input
qdot_out = []
for idx in range(0,len(tout)):
    Derivatives(zout[idx,:],tout[idx])
    qdot_out.append(Qdot)
    
plt.figure()
plt.plot(tout,qdot_out)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Qdot (BTU)')

plt.show()