import os
import csv

Budget_csv = os.path.join('Resources', 'budget_data.csv')
budget_dict = {}
delta_pnl = {}
results = []

def sum_pnl_func(budget_dict):
    sumpnl = 0    
    for key, value in budget_dict.items():
        sumpnl += float(value)

    return sumpnl

def delta_pnl_func(budget_dict, totMonths):
    start = 1
    total = 0
    for key, value in budget_dict.items():
        
        x = float(value)
        if start == 1:
            delta = 0
            delta_pnl[key] = delta
            start = 0
        else:
            delta = (x - y)
            delta_pnl[key] = delta
        y = x

        
    for key, value in delta_pnl.items():
        
        total = total + int(value)
    
    average = round(total/(totMonths-1),2)
    
    return average    

def max_profit(delta_pnl):
    maxprofit = 0

    for key, value in delta_pnl.items():
        
        if int(value) > maxprofit:
            maxprofit = int(value)
            maxmonth = key
    return maxmonth, maxprofit

def min_profit(delta_pnl):
    minprofit = 0

    for key, value in delta_pnl.items():

        if int(value) < minprofit:
            minprofit = int(float(value))
            minmonth = key
    return minmonth, minprofit

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
    header = next(Budget)
    
    budget_dict = {rows[0]:rows[1] for rows in Budget}

    totMonths = len(list(budget_dict))
    sumpnl = int(sum_pnl_func(budget_dict))
    average = delta_pnl_func(budget_dict, totMonths)
    max = max_profit(delta_pnl)
    min = min_profit(delta_pnl)
    output(totMonths,sumpnl, average,max,min)
        
    for line in results:
        print(line)
        
output_path = os.path.join('Analysis', 'Results.txt')

with open(output_path, "w") as datafile:
    
    for line in results:
        datafile.write(line)
        datafile.write('\n')

   