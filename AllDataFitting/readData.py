# import scipy.io as scio 
import numpy as np 
# import pandas as pd 
import matplotlib.pyplot as plt 

def readData(filepath="Capacity.txt"):
    with open(filepath,"r") as f:
        rawdata=f.read()
        rawdata=rawdata[:-1].split(" ")

    data=[]
    for capacity in rawdata:
        if capacity!="":
            data.append(eval(capacity))
    return data 

if __name__=="__main__":
    data=readData()
    # print(data)
    x=np.arange(0,len(data))
    failure=np.repeat(1.38,len(data))
    plt.plot(x,data)
    plt.plot(x,failure,color="r")
    plt.show()
