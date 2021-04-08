from readData import readData
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 
import math 


V_oc_array= readData("Voltage_Measure.txt")
I_array= readData("Current_Measure.txt")
Time= readData("Time.txt")
V_load= readData("Voltage_Load.txt")

for i in reversed(range(0,len(I_array))):
    if abs(I_array[i]) < 0.01:
        # print(i)
        I_array.pop(i)
        V_load.pop(i)
        Time.pop(i)
        V_oc_array.pop(i)

I={}
V_oc={}
for i in range(len(Time)):
	I[Time[i]] = I_array[i]
	V_oc[Time[i]] = V_oc_array[i]

initial=[0.5,0.5,100]

def func(tAll,R0,R1,C1):
	tau1=R1*C1
	# tau2=R2*C2
	global V_oc
	global I
	result=[]
	for t in tAll:
		temp= V_oc[t] + I[t]*R1*(1-math.exp(-t/tau1))
		result.append(temp)
	return np.array(result)

x=np.array(Time)
y=np.array(V_load)

param_bounds=(0,np.inf)

popt,pcov=curve_fit(func,x,y,p0=initial,bounds=param_bounds)

print("pcov: ",pcov)
R0=popt[0]
R1=popt[1]
C1=popt[2]
# R2=popt[3]
# C2=popt[4]
print("R0: ",R0)
print("R1: ",R1)
# print("R2: ",R2)
print("C1: ",C1)
# print("C2: ",C2)


yvals = func(x,R0,R1,C1)
plot1 = plt.plot(x, y, 'g',label='original values')
plot2 = plt.plot(x, yvals, 'r',label='fit values')
plt.xlabel("time(s)")
plt.ylabel("Voltage(v)")
plt.legend()
plt.show()