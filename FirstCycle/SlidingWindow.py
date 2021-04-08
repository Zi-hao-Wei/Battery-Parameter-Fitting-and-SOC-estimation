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

# initial=[0.05,0.05,100]

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
print(len(Time))


Capacity=0
for i in range(1,len(Time)):
	Capacity -= (Time[i]-Time[i-1])/3600*I[Time[i]]
SOC=[1]
SOCNow=1
for i in range(1,len(Time)):
	SOCNow=SOCNow+(Time[i]-Time[i-1])/3600*I[Time[i]]/Capacity
	# print(SOCNow)
	SOC.append(SOCNow)




lastR0=0
lastR1=0
lastC1=np.inf

AllR0=[]
AllR1=[]
AllC1=[]
c=[]
for i in range(8,178,20):
	c.append(SOC[i])
	x=np.array(Time[i-8:i+20])
	y=np.array(V_load[i-8:i+20])
	print(x,y)

	param_bounds=([lastR0,0,0],[np.inf,np.inf,lastC1])

	popt,pcov=curve_fit(func,x,y,bounds=param_bounds)

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

	AllR0.append(R0)	
	AllR1.append(R1)
	AllC1.append(C1)
	# print("C2: ",C2)
	lastR0=R0
	lastR1=R1
	lastC1=C1
	# initial=[lastR0,lastR1,lastC1]

plt.figure(1)
plt.subplot(311)
plt.scatter(c,AllR0,label="R0")
plt.ylabel("Ohm")
plt.legend()

plt.subplot(312)
plt.scatter(c,AllR1,label="R1")
plt.ylabel("Ohm")

plt.legend()
plt.subplot(313)
plt.scatter(c,AllC1,label="C1")
plt.xlabel("SOC")
plt.ylabel("F")

plt.legend()
plt.show()
