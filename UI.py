message1='Welcome to use our program Does Education Pay Off.' 
message2='This program will plot you the income distribution of each education level of undergrad, master, and Phd for a field of your choice.' 
message3='We will also then generate a custom plot to see when will your graduate education pay off, or if they pay off at all'
message4='Please choose a major from the following selection: '
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
        'General Medical Health Services']

str_build_majors = ''
for i in majors:
    str_build_majors += f'{i}\n'

str_build = f'{message1} \n\n{message2} \n{message3} \n\n{str_build_majors}'
print(str_build)

chosen_major = input(message4)

percentile_ug = input("Please enter percentile of undergrad: ")

upper_cut_off =input("Please eneter upper cutoff for percentile: ")

lower_cut_off = input("Please eneter lower cutoff for percentile" )

