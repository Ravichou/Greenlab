'''
LAB 3 - Carbon Aware Jobs - Level 1
You are the CTO of CloudCarbonInc, a company that is committed to reducing its carbon footprint.
CloudCarbonInc owns a datacenter, with limited capacity, that is powered by renewable energy sources.
Your mission is to schedule computing jobs in your datacenter while optimizing your carbon emissions.

Each job takes 1 minute to run and requires 1 core. 
The datacenter has a maximum of 10 cores.
The goal is to schedule these jobs over a 24-hour period. 

The carbon intensity of the datacenter's powergrid varies throughout the day and is provided as an input. 
In case of a tie, the job should be scheduled at the earliest possible time.

We consider a simplified scenario where the carbon intensity changes every hour for a total of 24 values. 
However, in the unit test provided, we use a smaller scheduling period for ease of testing.

Input: 
- the number of jobs to be scheduled, accessible as jobsNumber, 
- a list of 24 values indicating the carbon intensities at the datacenter for each hour of the day, accessible as carbonIntensity.

Output: a list of arrays, where each array consists of two elements: 
- the hour of the day (integer between 0 and 23) at which jobs are scheduled to run
- the number of jobs scheduled at that hour

See tests.py for examples of input/output.
'''

##### YOU CAN EDIT THE CODE BELOW #####

def scheduleJobs(exercise_input):
    jobsNumber = exercise_input['jobsNumber']
    carbonIntensity = exercise_input['carbonIntensity']

    # Create a list of tuples, each containing the hour and the corresponding carbon intensity
    
    # Sort carbon_intensity_dict by carbon intensity

    # Initialize the result list and the number of jobs left to schedule
    scheduledJobs = []
    
    # Schedule the jobs at the times with the lowest carbon intensity first
        
    return scheduledJobs

##### YOU CAN EDIT THE CODE ABOVE #####
##### DO NOT EDIT BELOW THIS LINE #####
#######################################

def run_func_test(tests):
    functional_test = tests['functional_test']
    scheduledJobs = scheduleJobs(functional_test)
    try:
        assert sum([job[1] for job in scheduledJobs]) == functional_test['jobsNumber'], f"Expected {functional_test['jobsNumber']} jobs scheduled but got {sum([job[1] for job in scheduledJobs])}"
    except AssertionError as e:
        print("Test FAILED with error: ")
        print(e)
    try:
        assert scheduledJobs == functional_test['expectedOutput'], f"Expected output {functional_test['expectedOutput']} \r\n but got {scheduledJobs}"
    except AssertionError as e:
        print("Test FAILED with error: ")
        print(e)
        return False
    print("Functional test PASSED")
    return True

def main(input):
    # Run the functional test
    print("Running functional test...")
    if run_func_test(input):
        print("Running Lab...")
        exercise = input['exercise']
        scheduledJobs = scheduleJobs(exercise)
        try:
            assert scheduledJobs == exercise['expectedOutput'], f"Expected \r\n {exercise['expectedOutput']} \r\n but got \r\n {scheduledJobs}"
            print("Level 1 COMPLETED.")
        except AssertionError as e:
            print("Level 1 FAILED.")
            print(e)