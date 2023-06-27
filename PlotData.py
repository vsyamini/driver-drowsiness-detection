import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os

fig = plt.figure('EAR',figsize=[5,3],dpi=100)
ax1 = fig.add_subplot(1,1,1)
fig1 = plt.figure('MAR',figsize=[5,3],dpi=100)
ax2 = fig1.add_subplot(1,1,1)

def animate(i):
    pullData = open("PreProcessed.txt","r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    zar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y,z = eachLine.split(',')
            xar.append(int(x))
            yar.append(float(y))
            zar.append(float(z))
    ax1.clear()
    ax1.plot(xar,yar)
    ax2.clear()
    ax2.plot(xar,zar)
    #ax1.set_xlim(0, 400)
    #ax1.set_ylim(0, 0.3)
    #ax1.set(xlim=(0, 500), ylim=(0.2, 0.40))
ani = animation.FuncAnimation(fig, animate, interval=1000)
ani1 = animation.FuncAnimation(fig1, animate, interval=1000)
plt.show()


#execfile('driverFatigue_v2.py')
