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