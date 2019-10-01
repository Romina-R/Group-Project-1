def master_plotting(major: str, percentile: float, upper:float, lower:float):

    majors=['Computer Science',
            'Mathematics' ,
            'Statistics and Decision Science', 
            'Chemical Engineering',
            'Civil Engineering',
            'Mechanical Engineering', 
            'Biology', 
            'Environmental', 
            'Chemistry', 
            'Economics', 
            'Political Science', 
            'Sociology', 
            'General Education', 
            'Law', 
            'Construction Services', 
            'Accounting', 
            'Finance', 
            'Marketing and Marketing Research', 
            'Pharmacy, Pharmaceutical Sciences and Administration',
            'Nursing', 
            'General Medical Health Services',
            'No_Degree']

    import pandas as pd
    import matplotlib.pyplot as plt 
    import numpy as np
    import scipy.stats as st
    from Plotting_Functions import intersection, plotline,warningmessage
    from Generate_data_dict import generate_data_dict
    from rominafunction import romina
    from Find_Y_Inter import findyinter
    path="Resources/US_Data.csv"
    tuition=[0, -24116, 2, -59116, 4, -24116]

    dictdata=generate_data_dict(path, upper, lower)
    majornames,incomes=romina(dictdata)


    if major=='all':
        for i in range(len(majors)):
            major=majornames[i]
            income=incomes[i]
            intercept=findyinter(income, tuition)
            plotline(income,intercept,major, percentile)
        else:
            i=majors.index(major)
            major=majornames[i]
            income=incomes[i]
            intercept=findyinter(income, tuition)
            plotline(income,intercept,major, percentile)