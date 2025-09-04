# Python3 program for implementation 
# of FCFS scheduling with Arrival Time

# Function to find the waiting 
# time for all processes
def findWaitingTime(processes, n, bt, arrival, wt):

    # waiting time for the first process is 0
    wt[0] = 0

    # calculating waiting time
    for i in range(1, n):
        wt[i] = bt[i - 1] + wt[i - 1] 

    # Adjust waiting time to consider arrival times
    for i in range(1, n):
        if arrival[i] > wt[i]:
            wt[i] = arrival[i]  # Process starts after its arrival time

# Function to calculate turn around time
def findTurnAroundTime(processes, n, bt, wt, tat):
    # calculating turnaround time by adding bt[i] + wt[i]
    for i in range(n):
        tat[i] = bt[i] + wt[i]

# Function to calculate average time
def findavgTime(processes, n, bt, arrival):

    wt = [0] * n
    tat = [0] * n 
    total_wt = 0
    total_tat = 0

    # Function to find waiting time of all processes
    findWaitingTime(processes, n, bt, arrival, wt)

    # Function to find turn around time for all processes
    findTurnAroundTime(processes, n, bt, wt, tat)

    # Display processes along with all details
    print( "Processes  Burst time  Arrival time  Waiting time  Turnaround time")

    # Calculate total waiting time and total turn around time
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        print(f"{processes[i]}\t\t{bt[i]}\t {arrival[i]}\t\t {wt[i]}\t\t {tat[i]}") 

    print("Average waiting time = " + str(total_wt / n))
    print("Average turn around time = " + str(total_tat / n))

# Driver code
if __name__ == "__main__":
    
    # process id's
    processes = [1, 2, 3]
    n = len(processes)

    # Burst time of all processes
    burst_time = [10, 5, 8]

    # Arrival time of all processes
    arrival_time = [0, 2, 4]

    # Call function to calculate average time
    findavgTime(processes, n, burst_time, arrival_time)
