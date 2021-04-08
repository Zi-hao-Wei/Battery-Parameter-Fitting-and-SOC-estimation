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
        print(i)
        I_array.pop(i)
        V_load.pop(i)
        Time.pop(i)
        V_oc_array.pop(i)
I={}
V_oc={}
for i in range(len(Time)):
	I[Time[i]] = I_array[i]
	V_oc[Time[i]] = V_oc_array[i]

Capacity=0
for i in range(1,len(Time)):
	Capacity -= (Time[i]-Time[i-1])/3600*I[Time[i]]
print(Capacity)
SOC=[1]
SOCNow=1
for i in range(1,len(Time)):
	SOCNow=SOCNow+(Time[i]-Time[i-1])/3600*I[Time[i]]/Capacity
	# print(SOCNow)
	SOC.append(SOCNow)


a=np.polyfit(SOC,V_oc_array,6)
b=np.poly1d(a)
print(a)
c=b(SOC)
plt.scatter(SOC,V_oc_array,marker='o',label='original datas')
plt.plot(SOC,c,ls='--',c='red',label='fitting with six-degree polynomial')
plt.xlabel("SOC")
plt.ylabel("V_OC(V)")
plt.legend()
plt.show()