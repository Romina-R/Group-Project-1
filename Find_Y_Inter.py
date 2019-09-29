def findyinter(madeupslope:list,tuition:list):
    under_1=tuition[1]
    under_2=0
    master_1=tuition[3]-tuition[2]*madeupslope[2]
    master_2=tuition[3]-tuition[2]*madeupslope[3]
    phd_1=tuition[5]-tuition[4]*madeupslope[4]
    phd_2=tuition[5]-tuition[4]*madeupslope[5]
    result=[under_1,under_2,master_1,master_2,phd_1,phd_2]
    return result
