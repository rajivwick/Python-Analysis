import os
import csv

election_csv = os.path.join('Resources', 'election_data.csv')
election_list = []
results = []
data_dict = {}      
output_results = {}


def update_new_total_func(value, totV, last):
    newtotal = int(value) + totV
    data_dict[last] = newtotal
    duplicate  = "y" 
    return duplicate  
   
def calc_percentage_func(election_list):
    
    last = "nil"
    totV = 0
    start = 0
    duplicate = "n"
    addTot = 0
    size = len(election_list)
    
    
    for row in election_list:


        if (row[2] != last and start == 1):
        
            addTot += 1
           
            for key,value in data_dict.items():
                
                if key == last:          
                    duplicate = update_new_total_func(value, totV, last)
                    
            if duplicate == "n":   
                data_dict[last] = totV
                totV = 1
                last = row[2]
            else:  
                totV = 1
                last = row[2] 
                #print("reset total happened after data_dict was adjusted due to duplicate")
        else:
            addTot += 1
            totV += 1
            last = row[2]
            start = 1
           
            if size == addTot:
                for key,value in data_dict.items():
                    if key == last:
                        duplicate = update_new_total_func( value, totV, last)            
            duplicate = "n"

    
    for key, value in data_dict.items():
        output_results[key] = value
    
    for key,value in data_dict.items():
        average = round((float(value) / size)*100,3)
        data_dict[key] = average
       
    for key,value in output_results.items():
        average = str(round((float(value) / size)*100,3)) + "%"+ " " + "(" + str(value) + ")"
        output_results[key] = average
            
def winner_func(data_dict):

    win_candidate = max(data_dict, key=data_dict.get)
    return win_candidate

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
    
    header = next(election)
    election_list = list(election)
    calc_percentage_func(election_list)
    winner = winner_func(data_dict)
    output_func(output_results, winner)
    
    for line in results:
        print(line)

output_path = os.path.join('Analysis', 'Results.txt')

with open(output_path, "w") as datafile:
    
    for line in results:
        datafile.write(line)
        datafile.write('\n')
    