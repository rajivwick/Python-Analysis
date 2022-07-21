#Dependencies
import os
import csv

#Import CSV file from Resource Folder
election_csv = os.path.join('Resources', 'election_data.csv')

#Global dictionaries and lists
election_list = []
results = []
data_dict = {}      
output_results = {}

#Function: (Duplicate) Created to print a new value against the key (Candidate) in the dictionary when a candidate is found duplicate times in the data set. 
def update_new_total_func(value, totV, last):
    newtotal = int(value) + totV
    data_dict[last] = newtotal
    duplicate  = "y" 
    return duplicate  

#Function: Iterate through the main data list, and then store the count of votes per candidate into a dictionary    
def calc_percentage_func(election_list):
    
    last = "nil"    #Initialized last, variable that is intended to hold the previous candidate name
    totV = 0        #Initialized to 0 - counter used to tally votes
    start = 0       #Initialized to 0 to allow for the first iteration not to trigger the first IF statement. 
    duplicate = "n" #Initialized to No - referencing we are not storing a duplicate key when updating data_dict
    addTot = 0      #Initialized to 0 - counter to tally number of iterations - used to determine the end of dataset.
    size = len(election_list)
    
    
    for row in election_list:

        #This candidate is met when we have reached a row where the candidate isn't the same as the previous row.
        if (row[2] != last and start == 1):
        
            addTot += 1  #count for every iteration.
            #Search the data_dict for whether the candidate being tallied is already within its dictionary 
            for key,value in data_dict.items():
                
                if key == last:
                    #If the candidate already has a value against it's key, then enter the duplicate function to update the value against that key and return the duplicate indicator.
                    duplicate = update_new_total_func(value, totV, last)
            #If the candidate isnt currently in the dictionary then add it and store the new value as the totV tallied.        
            if duplicate == "n":   
                data_dict[last] = totV
                totV = 1
                last = row[2]
            else:  
                totV = 1
                last = row[2] 
                
        else:
            addTot += 1 #count for every iteration.
            totV += 1
            last = row[2]
            start = 1   #Set start to 1 after the first iteration to allow for the first condition to be met when applicable. 
            #We need to make sure the data is saved once we reach the end of our list, we compare the iteration tally against the length of the list. 
            if size == addTot:
                for key,value in data_dict.items():
                    if key == last:
                        duplicate = update_new_total_func( value, totV, last)            
            duplicate = "n"

    #Created a copy of our data_dict to manipulate for output results.
    for key, value in data_dict.items():
        output_results[key] = value
    
    #Calculate average and store it into our data_dict
    for key,value in data_dict.items():
        average = round((float(value) / size)*100,3)
        data_dict[key] = average

    #Calculate the average and store it as a string in output_results   
    for key,value in output_results.items():
        average = str(round((float(value) / size)*100,3)) + "%"+ " " + "(" + str(value) + ")"
        output_results[key] = average

#Function: Finds the max value inside the data_dict, then stores and returns the key of this value.            
def winner_func(data_dict):

    win_candidate = max(data_dict, key=data_dict.get)
    return win_candidate

#Function: Creates results list - which is then used to print to terminal and txt file. Any future changes to output text, change within here. 
def output_func(output_results, winner):

    results.append("Election Results")
    results.append("-------------------------")
    results.append(f'Total Votes: {str(len(list(election_list)))}')
    results.append("-------------------------")
    for key, value  in output_results.items():
       results.append(str('%s: %s' % (key ,value)))
    results.append("-------------------------")
    results.append(winner)
    results.append("-------------------------")
    
    
with open(election_csv) as csvfile:
    
    election = csv.reader(csvfile, delimiter=',')
    #store titles as header variable
    header = next(election)
    #store the csv data as a list
    election_list = list(election)
    #calculate the percentage of votes each candidate received 
    calc_percentage_func(election_list)
    #store the winning candidates name 
    winner = winner_func(data_dict)
    #create results list
    output_func(output_results, winner)
    #output results on terminal
    for line in results:
        print(line)
  
output_path = os.path.join('Analysis', 'Results.txt')

with open(output_path, "w") as datafile:
    #output results to txt file
    for line in results:
        datafile.write(line)
        datafile.write('\n')
    