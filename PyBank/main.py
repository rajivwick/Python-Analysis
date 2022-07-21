#Dependencies
import os
import csv

#Import CSV file from Resource Folder
Budget_csv = os.path.join('Resources', 'budget_data.csv')

#Global dictionaries and lists
budget_dict = {}    # Created to store the Budget data as a Dictionary.
delta_pnl = {}      # Created to store a differences of PNL from month to month as a Dictionary.
results = []        # Created to store the final results in to a list. This list is then printed to terminal and txt file.

#Function: Imports the Budget dictionary, calculates the sum of all PNL values within the data set and exports the value.
#Operation: Iterates through the dictionary by the key (Month value) and adds the value (PNL value) to the 'sumpnl' variable.
def sum_pnl_func(budget_dict):
    sumpnl = 0    
    for key, value in budget_dict.items():
        sumpnl += float(value)

    return sumpnl

#Function: Imports the Budget dictionary and total months variable, calculates the difference of PNL between each month and returns the average.
def delta_pnl_func(budget_dict, totMonths):
    # Declare local variables
    start = 1   #This variable is to define the start of this calculation and is needed to allow the function to enter the first condition.
    total = 0   #This variable is used to store the total value within the created dictionary, delta_pnl. Initialized to start at 0.
    delta = 0   #This variable holds the value of the difference in PNL between the current and previous month.
    
    #Iterate through the budget dictionary
    for key, value in budget_dict.items():
        
        
        PNL = float(value)

        # This condition is set to allow the calculation to have the first difference in PNL be set to 0, as the first month has no comparison to find a difference against.
        if start == 1: 
            delta_pnl[key] = delta
            # As we have now concluded with the first key, we can set the start variable to 0.
            start = 0            
        
        else:
            delta = (PNL - Last_PNL)
            #Store this value into the delta_pnl dictionary, with the key (Month) being the same as the current key (Month) and the value to be the delta calculated above.
            delta_pnl[key] = delta
        #Set the Last_PNL variable to equal the current PNL before going into the next key(Month)
        Last_PNL = PNL
    #Iterate through delta_pnl    
    for key, value in delta_pnl.items():
        
        total = total + int(value)
    #Calculate the average 
    average = round(total/(totMonths-1),2)
    
    return average    

#Function: Import the delta_pnl dictionary and search through to determine the max profit difference store as a value, as well as the Month and returns both of this values.  
def max_profit(delta_pnl):
    maxprofit = 0

    for key, value in delta_pnl.items():
        
        if int(value) > maxprofit:
            maxprofit = int(value)
            maxmonth = key
    return maxmonth, maxprofit

#Function: Import the delta_pnl dictionary and search through to determine the min profit store as a value, as well as the Month and returns both of this values.  
def min_profit(delta_pnl):
    minprofit = 0

    for key, value in delta_pnl.items():

        if int(value) < minprofit:
            minprofit = int(float(value))
            minmonth = key
    return minmonth, minprofit

#Function: Imports all the necessary data to put into the results list which is then returned. 
#Function: Single point of result construction - If any changes are required for the output, edit here and results will print in terminal and on the txt file output.
def output(totMonths, sumpnl, average, max, min):
    
    results.append("Financial Analysis")
    results.append("----------------------------")
    results.append(f"Total Months: {str(totMonths)}")
    results.append(f"Total: ${str(sumpnl)}")
    results.append(f"Average Change: ${str(average)}")
    results.append(f"Greatest Increase in Profits: {str(max[0])} ({str(max[1])})")
    results.append(f"Greatest Decrease in Profits: {str(min[0])} ({str(min[1])})")

       
with open(Budget_csv) as csvfile:

    Budget = csv.reader(csvfile, delimiter=',')
    #Store title row as header list
    header = next(Budget)
    #Store the remaining csv into a dictionary, column 0 to denote our key(Months) and column 1 to denote our value(PNL)
    budget_dict = {rows[0]:rows[1] for rows in Budget}

    #Store the value of the length of the dictionary - number of rows of data
    totMonths = len(list(budget_dict))
    
    sumpnl = int(sum_pnl_func(budget_dict))

    average = delta_pnl_func(budget_dict, totMonths)
    #Store the values returned from the function as a list. [month, value]
    max = max_profit(delta_pnl)
   #Store the values returned from the function as a list. [month, value]
    min = min_profit(delta_pnl)
    #Creating the results list
    output(totMonths,sumpnl, average,max,min)
    #Outputting the results to terminal   
    for line in results:
        print(line)
        
output_path = os.path.join('Analysis', 'Results.txt')

with open(output_path, "w") as datafile:
    #Outputting the results to txt file  
    for line in results:
        datafile.write(line)
        datafile.write('\n')

   