'''
LAB 3 - Carbon Aware Jobs - Level 2
Good news! 
Thanks to its carbon reduction program, attracting many clients, CloudCarbonInc has expanded and now owns multiple datacenters across the globe.
Each datacenter has a different carbon intensity and computing capacity.
Your mission is to schedule computing jobs in your datacenter while optimizing your carbon emissions.

Each job still requires 1 core and takes 1 minute to complete. 
The jobs still have to be scheduled over a 24-hour period. 

The carbon intensity is now a matrix, which details the carbon intensity for each hour of the day for each datacenter' powergrid.

Input: 
- the number of jobs to be scheduled, accessible as jobsNumber, 
- a matrix of integers indicating the carbon intensity at each location for each hour of the day, accessible as carbonIntensity, 
- a list of integers indicating the number of available cores at each location, accessible as coreCapacity.
Locations are identified by their indices within these lists.

Output: a list of arrays, where each list represents a location with its scheduling plan. 
Each array consists of two elements: 
- the hour of the day (integer between 0 and 23) at which jobs are scheduled to run, 
- the number of jobs scheduled at that hour.

See tests.py for examples of input/output.
'''  

##### YOU CAN EDIT THE CODE BELOW #####

def scheduleJobs(exercise_input):
    # Extracting parameters
    jobsNumber = exercise_input['jobsNumber']
    coreCapacity = exercise_input['coreCapacity']
    carbonIntensity = exercise_input['carbonIntensity']
    
    # Initialize the scheduling plan
    scheduledJobs = [[] for _ in coreCapacity]
    
    # Schedule the jobs at the times with the lowest carbon intensity first
    
    # Return the result
    return scheduledJobs

##### YOU CAN EDIT THE CODE ABOVE #####
##### DO NOT EDIT BELOW THIS LINE #####
#######################################

def run_func_test(tests):
    functional_test = tests['functional_test']
    scheduledJobs = scheduleJobs(functional_test)
    try:
        sumScheduledJobs = 0
        for location in scheduledJobs: # need to sum on all locations
            for job in location:
                assert job[0] >= 0 and job[0] <= 23, f"Expected hour to be between 0 and 23 but got {job[0]}"
                sumScheduledJobs += job[1]
        assert sumScheduledJobs == functional_test['jobsNumber'], f"Expected {functional_test['jobsNumber']} jobs scheduled but got {sumScheduledJobs}"
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
            sumScheduledJobs = 0
            for location in scheduledJobs: # need to sum on all locations
                for job in location:
                    assert job[0] >= 0 and job[0] <= 23, f"Expected minute to be between 0 and 23 but got {job[0]}"
                    sumScheduledJobs += job[1]
            assert sumScheduledJobs == exercise['jobsNumber'], f"Expected {exercise['jobsNumber']} jobs scheduled but got {sumScheduledJobs}"
            assert scheduledJobs == exercise['expectedOutput'], f"Expected \r\n {exercise['expectedOutput']} \r\n but got \r\n {scheduledJobs}"
            print("Level 2 COMPLETED.")
        except AssertionError as e:
            print("Level 2 FAILED.")
            print(e)