from readData import readData
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 
import math 

AllR0=[]
AllR1=[]
AllR2=[]
AllC1=[]
AllC2=[]
lastR0=0.2
lastR1=0.0003
lastC1=np.inf
c=[]
initial=[1,1,100]
for i in range(0,100,10):
# i=1
    c.append(i)
    V_oc_array= readData(".//AllData//Voltage_Measure"+str(i)+".txt")
    I_array= readData(".//AllData//Current_Measure"+str(i)+".txt")
    Time= readData(".//AllData//Time"+str(i)+".txt")
    V_load= readData(".//AllData//Voltage_Load"+str(i)+".txt")

    # capacity=0

    for j in reversed(range(0,len(I_array))):
        if abs(I_array[j]) < 0.01:
            # print(i)
            I_array.pop(j)
            V_load.pop(j)
            Time.pop(j)
            V_oc_array.pop(j)



    I={}
    V_oc={}
    for i in range(len(Time)):
    	I[Time[i]] = I_array[i]
    	V_oc[Time[i]] = V_oc_array[i]




    def func(tAll,R0,R1,C1):
    	tau1=R1*C1
    	global V_oc
    	global I
    	result=[]
    	for t in tAll:
    		temp= V_oc[t] + I[t]*R1*(1-math.exp(-t/tau1))+R0*I[t]
    		result.append(temp)
    	return np.array(result)

    x=np.array(Time)
    y=np.array(V_load)


    param_bounds=([lastR0,lastR1,0],[np.inf,np.inf,np.inf])

    popt,pcov=curve_fit(func,x,y,p0=initial,bounds=param_bounds)
    print("pcov: ",pcov)
    R0=popt[0]
    R1=popt[1]
    C1=popt[2]
    print(R0,R1,C1)

    lastR0=R0
    lastR1=R1
    lastC1=C1

    AllR0.append(R0)
    AllR1.append(R1)
    AllC1.append(C1)

    # yvals = func(x,R0,R1,C1)
    # plot1 = plt.plot(x, y, 'g',label='original values')
    # plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
    # plt.show()



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
plt.xlabel("Cycle")
plt.ylabel("F")

plt.legend()
plt.show()
