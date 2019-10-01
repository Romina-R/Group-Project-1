import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import scipy.stats as st
import math
tuition=[0, -96464, 2, -166464, 4, -96464]

# madeupslope=[45000, 55000, 65000, 85000, 88000, 112000]
# madeupintercept=[-45000,-205000,-245000,-345000,-425000]
# madeuplegend='Fine Art'

def findyinter(madeupslope:list,tuition:list):
    under_1=tuition[1]
    under_2=0
    master_1=tuition[3]-tuition[2]*madeupslope[2]
    master_2=tuition[3]-tuition[2]*madeupslope[3]
    phd_1=tuition[5]-tuition[4]*madeupslope[4]
    phd_2=tuition[5]-tuition[4]*madeupslope[5]
    result=[under_1,under_2,master_1,master_2,phd_1,phd_2]
    return result

def romina(madeupdata:dict):
    degree = []

    listofsalaryrange = []
    for x in madeupdata:
        degree.append(x)
        salaryrange=[]

        for i in range(len(madeupdata[x])):


                if (i)%2 == 0:
                # print(madeupdata[x][i])
                    salaryrange.append(madeupdata[x][i]-madeupdata[x][i+1])
                    salaryrange.append(madeupdata[x][i]+madeupdata[x][i+1])
        
        listofsalaryrange.append(salaryrange) 

    return degree, listofsalaryrange


def warningmessage(minvalue:float,maxvalue:float):
    if minvalue<0 & maxvalue<0:
        warning='Bro you wasting your time'
    if minvalue>0 & maxvalue<0:
        warning='Good luck you might break even'
    if minvalue>0 & maxvalue>50:
        warning='Good luck you might break even'
    if minvalue>0 & max<50:
        warning='Grats you are interested in the right thing'
    return warning

def intersection(a1:float,b1:float,a2:float,b2:float):
    #find the intersection of lines y1=a1*x+b1 and y2=a2*x+b2
    x=(b2-b1)/(a1-a2)
    y=a1*x+b1
    return(x,y)

def plotline(slope:list, yintercept:list,legend:str, percentile:float):
#plot a line with known slope and y intercept
    undergrad_mean=(slope[1]+slope[0])/2
    undergrad_std=(slope[1]-slope[0])/2
    zscore=st.norm.ppf(percentile)
    slope1=undergrad_mean+(zscore*undergrad_std)
    
#Find the percentile of master and Phd to break even with undergrand income:
    master_z=(undergrad_mean-(slope[2]+slope[3])/2)/((slope[3]-slope[2])/2)
    phd_z=((undergrad_mean-(slope[4]+slope[5])/2)/((slope[5]-slope[4])/2))
    master_p=.5 * (math.erf(master_z / 2 ** .5) + 1)
    phd_p=.5 * (math.erf(phd_z / 2 ** .5) + 1)
    master_z_yint=tuition[3]-tuition[2]*undergrad_mean
    phd_z_yint=tuition[5]-tuition[4]*undergrad_mean


# Find the intersection of the lines.
    master_1 = intersection(slope1, yintercept[0], slope[2], yintercept[2])
    master_2 = intersection(slope1, yintercept[0], slope[3], yintercept[3]) 
    
    phd_1 = intersection(slope1, yintercept[0], slope[4], yintercept[4])
    phd_2 = intersection(slope1, yintercept[0], slope[5], yintercept[5])
    
# Dynamic Range for master degree plot to make the plot look more focused and nicer.
    master_axis_1 = master_1[0] 
    master_axis_2 = master_2[0] 
    master_axis = max(master_axis_1,master_axis_2)
# Prevent if the degree never pays off.
    if master_axis>50:
        master_axis=50
    master_range = np.arange(2, master_axis+5 , 1)
    under_range_1 = np.arange(0, master_axis+5 , 1)

# Dynamic Range for Phd degree plot to make the plot look more focused and nicer.    
    phd_axis_1 = phd_1[0]
    phd_axis_2 = phd_2[0] 
    phd_axis = max(phd_axis_1, phd_axis_2)
# Prevent if the degree never pays off.
    if phd_axis>50:
        phd_axis=50
    phd_range = np.arange(4, phd_axis+5 , 1)
    under_range_2 = np.arange(0, phd_axis+5 , 1)
    
# Undergrad Lines
    y1=under_range_1*slope1+yintercept[0]
    y11=under_range_2*slope1+yintercept[0]
    
# Master Lines
    y2=master_range*slope[2]+yintercept[2]
    y3=master_range*slope[3]+yintercept[3]
    y33=master_range*undergrad_mean+master_z_yint
    
# Phd Lines 
    y4=phd_range*slope[4]+yintercept[4]
    y5=phd_range*slope[5]+yintercept[5]
    y44=phd_range*undergrad_mean+phd_z_yint
    
    bottom=0.25
    left=0.15
    figuresize=(9,6)
    plt.figure(figsize=(figuresize))
    plt.gcf().subplots_adjust(bottom=bottom)
    plt.gcf().subplots_adjust(left=left)
    
    plt.tight_layout() 
    plt.plot(under_range_1, y1,'b-.',label=f"Undergrad Income At {round(percentile*100, 1)} Percentile",linewidth=4,)
    plt.plot(master_range, y3 ,'r',label="Master Income + Standard Deviation",linewidth=2,)
    plt.plot(master_range, y2 ,'m',label="Master Income - Standard Deviation",linewidth=2,)
    plt.plot(master_range, y33 ,'y',label="Master Income Equals to Undergrad",linewidth=2,)
    
    

    plt.legend()
    plt.title(f"{legend} Undergrad vs Master Income") 
    plt.xlabel(f"It will take {int(master_2[0]-2)} to {int(master_1[0]-2)} Years to break even with {round(percentile*100, 1)} percentile of Undergrad.\nYou need to be as good as {round(master_p*100, 1)} percentile of masters to make the same as undergrad at {round(percentile*100, 1)} percentile.\n Years Out of College")
    plt.ylabel("Accumulate Income $")
    # Set the starting range from 0 to make plot look better.
    plt.xlim(0, master_axis+5)
    plt.ylim(bottom=-170000)
    plt.hlines(y=master_2[1], xmin=0, xmax=master_2[0], linewidth=2, color='darkgreen', linestyles='dotted')
    plt.hlines(y=master_1[1], xmin=0, xmax=master_1[0], linewidth=2, color='darkgreen', linestyles='dotted')
    
    # Need to get ymax because for axvline ymax is a fraction of the y max value, so ymax>=1 would plot to the top.
    xmin, xmax, ymin, ymax = plt.axis()
    plt.axvline(x=master_2[0], ymin=0, ymax=(master_2[1]/ymax),color='darkgreen', linestyle = '--')
    plt.axvline(x=master_1[0], ymin=0, ymax=(master_1[1]/ymax),color='darkgreen', linestyle = '--')   
    
    plt.scatter(master_2[0],master_2[1],marker="X", c='darkgreen',s=500)
    plt.scatter(master_1[0],master_1[1],marker="X", c='darkgreen',s=500)
    path1=f"Images/{legend}_Undergrad_vs_Master_Income"
    plt.show()
    plt.savefig(path1)
    
    
    plt.figure()
    plt.gcf().subplots_adjust(bottom=bottom)
    plt.gcf().subplots_adjust(left=left)
    plt.figure(figsize=(figuresize))
    plt.tight_layout()
    plt.plot(under_range_2,y11,'b-.',label=f"Undergrad Income At {round(percentile*100, 2)} Percentile",linewidth=4,)
    plt.plot(phd_range,y5,'r',label="Phd Income + Standard Deviation",linewidth=2,)
    plt.plot(phd_range,y4,'m',label="Phd Income - Standard Deviation",linewidth=2,)
    plt.plot(phd_range, y44 ,'y',label="Master Income Equals to Undergrad",linewidth=2,)
    

    plt.legend()
    plt.title(f"{legend} Undergrad vs Phd Income") 
    plt.xlabel(f"It will take {int(phd_2[0]-2)} to {int(phd_1[0]-2)} Years to break even with {round(percentile*100, 1)} percentile of Undergrad.\nYou need to be as good as {round(phd_p*100, 1)} percentile of Phds to make the same as undergrad at {round(percentile*100, 1)} percentile.\n Years Out of College")
    plt.ylabel("Accumulate Income $") 
    # Set the starting range from 0 to make plot look better.
    plt.xlim(0, phd_axis+5)
    plt.ylim(bottom=-100000)
    plt.hlines(y=phd_2[1], xmin=0, xmax=phd_2[0], linewidth=2, color='darkgreen', linestyles='dotted')
    plt.hlines(y=phd_1[1], xmin=0, xmax=phd_1[0], linewidth=2, color='darkgreen', linestyles='dotted')
    
    # Need to get ymax because for axvline ymax is a fraction of the y max value, so ymax>=1 would plot to the top.
    xmin, xmax, ymin, ymax = plt.axis()
    plt.axvline(x=phd_2[0], ymin=0, ymax=(phd_2[1]/ymax),color='darkgreen', linestyle = '--')
    plt.axvline(x=phd_1[0], ymin=0, ymax=(phd_1[1]/ymax),color='darkgreen', linestyle = '--') 
    
    plt.scatter(phd_2[0],phd_2[1],marker="X", c='darkgreen',s=500)
    plt.scatter(phd_1[0],phd_1[1],marker="X", c='darkgreen',s=500)
    path2=f"Images/{legend}_Undergrad_vs_Phd_Income"
    plt.show()
    plt.savefig(path2)
    
    plt.figure()
    plt.gcf().subplots_adjust(bottom=bottom)
    plt.gcf().subplots_adjust(left=left)
    plt.figure(figsize=(figuresize))
    plt.tight_layout() 

    
