'''
LAB 3 - Carbon Aware Jobs - Level 3
More great news ! You continue expanding your cloud computing empire !
However, to simplify your operations, you decided to sell your datacenters and now rent them from different suppliers, based on different hardware configurations.
How will CloudCarbonInc manage to schedule jobs across all these datacenters, while optimizing carbon emissions ?

You now have to optimize not only the carbon intensity, but also the embodied emissions of the servers used, to optimize the total carbon emissions of your operations.

For the Energy consumption:
We assume all the cores in all the datacenters have equivalent capabilities and have the same power consumption.

For the Carbon Intensity:
The carbon intensity is still a matrix, which details the carbon intensity for each hour of the day for each datacenter' powergrid.

For the Embodied Emissions:
EL is fixed to 4 years for all datacenters.
There is one TE and one ToR for each datacenter.

As a reminder: 
SCI = (O + M)/R = (E x I + TE x (TiR/EL) x (RR/ToR) )/R

Each job still requires 1 core and takes 1 minute to complete. 
The jobs still have to be scheduled over a 24-hour period. 

Input: 
- the number of jobs to be scheduled, accessible as jobsNumber, 
- a matrix of integers indicating the carbon intensity at each location for each hour of the day, accessible as carbonIntensity, 
- a list of integers indicating the number of available cores at each location, accessible as coreCapacity.
- a list of integers indicating the TE for each location, accessible as embodiedTE.
- a list of integers indicating the ToR for each location, accessible as embodiedToR.
Locations are identified by their indices within these lists.

Output: a list of arrays, where each list represents a location with its scheduling plan. 
Each array consists of two elements: 
- the hour of the day (integer between 0 and 23) at which jobs are scheduled to run, 
- the number of jobs scheduled at that hour.

See tests.py for examples of input/output.
'''

##### YOU CAN EDIT THE CODE BELOW #####

def computeSciPerJob():
    '''Calculate normalized emissions per job'''


    return 
    


def scheduleJobs(exercise_input):
    # Extracting parameters
    jobsNumber = exercise_input['jobsNumber']
    coreCapacity = exercise_input['coreCapacity']
    carbonIntensity = exercise_input['carbonIntensity']
    embodiedTE = exercise_input['embodiedTE']
    toR = exercise_input['ToR']
    power_per_core = 3

    merged_carbon_intensities = []
    
    # Initialize the scheduling plan
    scheduledJobs = [[] for _ in coreCapacity]
    
    # Implement your code here

    # Return the result in a list of arrays
    return scheduledJobs

##### YOU CAN EDIT THE CODE ABOVE #####
##### DO NOT EDIT BELOW THIS LINE #####
#######################################



def run_func_test(tests):
    functional_test = tests['functional_test']
    scheduledJobs = scheduleJobs(functional_test)
    try:
        import src.Lab3Utils as lab3_utils
        lab3_utils.print_schedule_comparison(scheduledJobs, functional_test['expectedOutput'])
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
    import src.Lab3Utils
    print("Running functional test...")
    if run_func_test(input):
        print("Running Lab...")
        exercise = input['exercise']
        scheduledJobs = scheduleJobs(exercise)
        try:
            sumScheduledJobs = 0
            for location in scheduledJobs: # need to sum on all locations
                for job in location:
                    assert job[0] >= 0 and job[0] <= 23, f"Expected hour to be between 0 and 23 but got {job[0]}"
                    sumScheduledJobs += job[1]
            assert sumScheduledJobs == exercise['jobsNumber'], f"Expected {exercise['jobsNumber']} jobs scheduled but got \r\n \r\n {sumScheduledJobs}"
            assert scheduledJobs == exercise['expectedOutput'], f"Expected \r\n {exercise['expectedOutput']} \r\n \r\n \r\n but got \r\n \r\n \r\n {scheduledJobs}"
            results = src.Lab3Utils.compare_emissions(scheduledJobs, exercise['jobsNumber'], 
                          exercise['carbonIntensity'],
                          exercise.get('coreCapacity'))
            src.Lab3Utils.print_comparison_results(results)
            print("Level 3 COMPLETED.")
        except AssertionError as e:
            print("Level 3 FAILED.")
            print(e)