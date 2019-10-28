# MRT flow simulator for the payload

import numpy as np
import matplotlib.pyplot as plt
#units are metric

def convert_inm(inches):
    return inches / 39.37

diameter1 = 1 / 4 #in
diameter_m1 = convert_inm(diameter1) #conversion to metric
# print(diameter_m1)
r = diameter_m1 / 2
L = 4.2672
A = np.pi * r * r
q_sea = 13.5

percentage = (101600 - ((8 * 0.00001789 * L * (q_sea / 60000)) / (np.pi * (r**4)))) / 101600
#print(percentage)

# Data for the respective altitudes
alt = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000, 30000, 35000, 40000]
rho = [1.225, 1.112, 1.007, 0.9093, 0.8194, 0.7364, 0.6601, 0.5900, 0.5258, 0.4671, 0.4135, 0.1948, 0.08891, 0.04008, 0.01841, 0.01182, 0.003996]
mu = [0.00001789, 0.00001758, 0.00001726, 0.00001694, 0.00001661, 0.00001628, 0.00001595, 0.00001561, 0.00001527, 0.00001493, 0.00001458, 0.00001422, 0.00001422, 0.00001448, 0.00001475, 0.00001434, 0.00001601]
p1 = [101600, 97700, 94200, 90800, 87500, 84300, 81200, 78200, 75300, 72400, 69700, 57200, 46600, 37600, 30100, 23800, 18700]

# Assuming constant delta p percentage
p2 = []
for i in range(len(p1)):
    p2.append(p1[i] * percentage)

delta_p = np.subtract(p1, p2) # assuming constant delta p percentage and q_sea lpm at sea level
#print(delta_p)

# Calculating individual values for the Hagen–Poiseuille equation
Q = []
v = []
for i in range(len(delta_p)):
    Q.append(60000 * ((delta_p[i] * np.pi * (r**4)) / (8 * mu[i] * L)))
    v.append((Q[i] / 60000) / A)
    
coefs = np.polyfit(alt, Q, 4)
#print(coefs)
def polynomial(x, coef):
    output = 0
    for i in range(len(coef)):
        order_index = (len(coef) -1) - i
        output += coef[i] * x**(order_index)
    return output


#plt.plot(alt, p1, 'o')
print('Flow rates (lpm):', Q)
print('Velocities (m/s): ', v)
plt.plot(alt, Q, 'o')
plt.plot(np.linspace(0, 40000), polynomial(np.linspace(0, 40000), coefs))
plt.title('Theoretical Flow Rate by Altitude')
plt.xlabel('Altitude (ft)')
plt.ylabel('Flow Rate (lpm)')
plt.savefig('flowrate_alt.jpg', dpi=300)

#plt.plot(alt, v)
#plt.title('Theoretical Airspeed by Altitude')
#plt.xlabel('Altitude (ft)')
#plt.ylabel('Velocity (m/s)')
