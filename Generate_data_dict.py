#!/usr/bin/env python
# coding: utf-8

# # Import Libaries and fetch data

import pandas as pd
import numpy as np

def generate_data_dict(path, upper, lower):

    #path="Resources/US_Data.csv"
    fields = ['FOD1P','SCHL','WAGP','AGEP','COW']
    coarse_data=pd.read_csv(path, skipinitialspace=True, usecols=fields)
    coarse_data['FOD1P'] = coarse_data['FOD1P'].astype(str)
    coarse_data.head()

    coarse_data['FOD1P'].value_counts()

    education_attainment = [24.0,22.0,21.0]
    refined_data = coarse_data.loc[coarse_data['SCHL'].isin(education_attainment)].copy()
    refined_data['SCHL'].value_counts()

    refined_data.head()

    bachelors_tuition = 24116
    masters_tuition = 35000
    phd_tuition = 0
    refined_data["Tuition"] = np.where(refined_data.SCHL == 21.0, bachelors_tuition,
                                    np.where(refined_data.SCHL == 22.0, masters_tuition,
                                            np.where(refined_data.SCHL == 24.0, phd_tuition, "NA")))

    refined_data["SCHL"] = np.where(refined_data.SCHL == 21.0, "Bachelors_Degree",
                                    np.where(refined_data.SCHL == 22.0, "Masters_Degree",
                                            np.where(refined_data.SCHL == 24.0, "PHD", "NA")))
    refined_data.head()

    refined_data["SCHL"].value_counts()

    degree_dict={'2102.0':'Computer Science',
                '3700.0':'Mathematics' ,
                '3702.0':'Statistics and Decision Science', 
                '2405.0':'Chemical Engineering',
                '2406.0':'Civil Engineering',
                '2414.0':'Mechanical Engineering', 
                '3600.0':'Biology', 
                '1301.0':'Environmental', 
                '5003.0':'Chemistry', 
                '5501.0':'Economics', 
                '5506.0':'Political Science', 
                '5507.0':'Sociology', 
                '2300.0':'General Education', 
                '3202.0':'Law', 
                '5601.0':'Construction Services', 
                '6201.0':'Accounting', 
                '6207.0':'Finance', 
                '6206.0':'Marketing and Marketing Research', 
                '6108.0':'Pharmacy, Pharmaceutical Sciences and Administration',
                '6107.0':'Nursing', 
                '6100.0':'General Medical Health Services',
                'No_Degree':'No_Degree'}
    refined_data['FOD1P'] = refined_data['FOD1P'].map(degree_dict)
    refined_data.head()

    refined_data['FOD1P'].value_counts()

    # rename columns
    rename_df = refined_data.copy()
    rename_df.rename(columns = {'FOD1P':'Field of Study', 
                                'SCHL':'Educational Attainment', 
                                'WAGP':'Income', 'AGEP':'Age', 
                                'COW':'Class of Worker'}, inplace=True)
    rename_df.head(10)
    
    # Extra magic trick from Steve to cut off the top percentiles
    # Delete all the negative incomes cause they are probably doing some business
    rename_df=rename_df[rename_df['Income']>0]
    # Find top percentile
    income_percentile=rename_df.groupby(['Field of Study', 'Educational Attainment' ])['Income'].quantile(upper)
    pindex=income_percentile.index
    for i in range(len(pindex)):
        rename_df.loc[(rename_df['Field of Study'] == pindex[i][0]) & 
                                  (rename_df['Educational Attainment'] == pindex[i][1]) & 
                                 (rename_df['Income'] >= income_percentile[i]), ['Income']]=999999999
    rename_df=rename_df[rename_df['Income']!=999999999]
    
    
    # Find bottom percentile
    income_percentile=rename_df.groupby(['Field of Study', 'Educational Attainment' ])['Income'].quantile(lower)
    pindex=income_percentile.index
    for i in range(len(pindex)):
        rename_df.loc[(rename_df['Field of Study'] == pindex[i][0]) & 
                                  (rename_df['Educational Attainment'] == pindex[i][1]) & 
                                 (rename_df['Income'] <= income_percentile[i]), ['Income']]=999999999
    rename_df=rename_df[rename_df['Income']!=999999999]

    
    


    # # Create DataFrames for plotting

    # ### for mean data

    comment = '''    
    What I need:
    dictionary_template = { "Field0":[bachelor_income_mean, bachelor_income_std, 
                                    master_income_mean, master_income_std,
                                    phd_income_mean, phd_income_std ],
                            "Field1":[bachelor_income_mean, bachelor_income_std, 
                                    master_income_mean, master_income_std,
                                    phd_income_mean, phd_income_std ], .... }
    '''
    field_mean_std_df = rename_df.copy()
    mean_sr = field_mean_std_df.groupby(['Field of Study', 'Educational Attainment' ])['Income'].mean()
    mean_df = mean_sr.to_frame()
    # rounding the mean values to 2 decimal places
    mean_df.rename(columns={'Income':'Mean'}, inplace=True)
    mean_df['Mean'] = mean_df['Mean'].apply(lambda x: round(x, 2))
    mean_df

    #for display
    mean_pivt = mean_df.pivot_table(index='Educational Attainment', columns='Field of Study', values='Mean')
    mean_pivt

    # ### for std data

    std_sr = field_mean_std_df.groupby(['Field of Study', 'Educational Attainment' ])['Income'].std()
    std_df = std_sr.to_frame()
    # rounding the mean values to 2 decimal places
    std_df.rename(columns={'Income':'std'}, inplace=True)
    std_df['std'] = std_df['std'].apply(lambda x: round(x, 2))
    std_df

    #for display
    std_pivt = std_df.pivot_table(index='Educational Attainment', columns='Field of Study', values='std')
    std_pivt

    mean_df_cpy = mean_df.copy()
    std_df_cpy = std_df.copy()
    mean_df_cpy.reset_index(inplace=True)
    std_df_cpy.reset_index(inplace=True)
    # create consolidated dictionary for plotting
    data_dict = {}
    FOS_list = mean_df_cpy['Field of Study'].unique().tolist()

    #std_df_cpy[std_df_cpy['Field of Study'] == 'Nursing']
   
    for fos in FOS_list:
        bs_mean = mean_df_cpy[(mean_df_cpy['Field of Study'] == fos) &            (mean_df_cpy['Educational Attainment'] == 'Bachelors_Degree')]['Mean'].tolist()[0]
        bs_std = std_df_cpy[(std_df_cpy['Field of Study'] == fos) &            (std_df_cpy['Educational Attainment'] == 'Bachelors_Degree')]['std'].tolist()[0]
        
        ms_mean = mean_df_cpy[(mean_df_cpy['Field of Study'] == fos) &            (mean_df_cpy['Educational Attainment'] == 'Masters_Degree')]['Mean'].tolist()[0]
        ms_std = std_df_cpy[(std_df_cpy['Field of Study'] == fos) &            (std_df_cpy['Educational Attainment'] == 'Masters_Degree')]['std'].tolist()[0]
        
        phd_mean = mean_df_cpy[(mean_df_cpy['Field of Study'] == fos) &            (mean_df_cpy['Educational Attainment'] == 'PHD')]['Mean'].tolist()[0]
        phd_std = std_df_cpy[(std_df_cpy['Field of Study'] == fos) &            (std_df_cpy['Educational Attainment'] == 'PHD')]['std'].tolist()[0]
        
        data_dict[fos] = [bs_mean, bs_std, ms_mean, ms_std, phd_mean, phd_std]
        
    comment = '''
    The data_dict template is:
    {<field labe>:<list of values>}
    {'Field of study':[ bachelors_degree_mean, bachelors_degree_std, 
                        masters_degree_mean, masters_degree_std, 
                        PhD_mean, PhD_std ]  
    }
    '''    
    #from pprint import pprint
    #pprint(data_dict)

    data_df = pd.DataFrame(data_dict)


    return data_dict