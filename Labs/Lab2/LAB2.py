'''
LAB 2 - Implement Software Carbon Intensity - Solution
You will now do an implementation of the GSF’s Software Carbon Intensity (SCI) formula and evaluate the carbon emissions of running software. 
You will rely only on the open source Cloud Carbon Footprint (CCF) specs:
https://www.cloudcarbonfootprint.org/docs/methodology/#summary

A set of data is provided in input. 
These data represent the resources utilization of an application running in Microsoft Azure over a given period of time.

You will have to determine:
- the power consumption of each hardware resource,
- the embodied emissions,
- the total carbon emissions.
There is a bonus section for calculating the energy consumption of network and storage resources.

Hypothesis:
- The job is monothreaded.
- We assume the computation is executed in Azure, Microsoft's Cloud Service Provider, on a DS2 v2 Virtual Machine, of the D1s-5s v2 series.
- For each constant, consider the average values corresponding to the Cloud Service Provider.
- For the memory energy consumption, we will consider that none of it was implicitly included in the CPU energy consumption, and thus will consider all the given value in the input as excess memory.
- For the carbon intensity, we will consider a constant value of the region (West Europe) where the Azure cluster is deployed.
- Load factor is not provided. Fallback to the average value.
- Beware of the Azure PUE! Take the worst average value documented.
- In the Embodied Emissions formula, the TR factors represent different SCI factors.
'''
###########################################################
############### YOU CAN EDIT THE CODE BELOW ###############

# CPU constants
CPU_MIN_W = 0  # Minimum power consumption of one CPU core - 0% load (Watts)
CPU_MAX_W = 0  # Maximum power consumption of one CPU core - 100% load (Watts)
CPU_LOAD = 0  # CPU load factor (no unit)

def calculate_e_cpu(cpu_time_s, cores_requested, cpu_load = CPU_LOAD):
    E_cpu_Ws = 0
    return E_cpu_Ws # in Ws, rounded to 3 decimals

# Memory constant
MEM_COEF = 0  # Power consumption of 1 GB of memory (W/GB)

def calculate_e_mem(memory_MB, execution_time_s):
    E_mem_Ws = 0
    return E_mem_Ws # in Ws, rounded to 3 decimals

# Embodied Emissions constants
TE = 0 # Total lifecycle emissions of the hardware for a DS2 v2 Virtual Machine, of the D1s-5s v2 series (kgCO2)
EL = 0 # Expected lifespan of the hardware (seconds)
RR = 0 # Number of resources reserved for use by the job (vCPUs)
TR = 0 # Total number of resources available (vCPUs)

def calculate_m(execution_time_s):
    M_mgCO2 = 0
    return M_mgCO2 # in mgCO2, rounded to 3 decimals

# Carbon intensity and PUE constants
I = 0 # Carbon intensity (kgCO2/Ws, converted from tonCO2/kWh. 1 kWh = 1.000 Wh = 1.000 * 3.600 Ws)
PUE = 0 # Power Usage Effectiveness, a measure of data center energy efficiency. Use the Azure best value. (no unit)

def calculate_sci(E_cpu_Ws, E_mem_Ws, M_mgCO2, E_network_Ws = 0, E_storage_Ws = 0):
    SCI = 0
    return SCI # in mgCO2, rounded to 2 decimals

############ BONUS SECTION ############
# Network constants
NTW_EXT_COEF = 0 # Power consumption of external data transfer (kWh/GB)
NTW_INT_COEF = 0 # Power consumption of internal data transfer (kWh/GB)

def calculate_e_network(external_data_transfer_MB, internal_data_transfer_MB):
    E_network_Ws = 0
    return E_network_Ws # in Ws, rounded to 3 decimals

# Storage constants
REPLICATION_FACTOR = 0 # Storage replication factor for Azure disk (no unit)
STORAGE_COEF = 0 # Energy consumption of 1 TB of SSD storage (Wh/TBh)

def calculate_e_storage(storage_MB, execution_time_s):
    E_storage_Ws = 0
    return E_storage_Ws # in Ws, rounded to 3 decimals
############ / BONUS SECTION ############

############### DO NOT EDIT BELOW THIS LINE ###############
###########################################################

def SCI_service(cpu_time_s, memory_MB, cpu_load = CPU_LOAD):
    E_cpu = calculate_e_cpu(cpu_time_s, 1, cpu_load)
    E_mem = calculate_e_mem(memory_MB, cpu_time_s)
    M = calculate_m(cpu_time_s)
    SCI = calculate_sci(E_cpu, E_mem, M)
    if SCI == 0:
        return "NOT IMPLEMENTED!"
    return SCI

def main(tests):
    # Calculate values
    E_cpu_Ws = calculate_e_cpu(tests.input['cpu_time_s'], tests.input['cores_requested'])
    E_mem_Ws = calculate_e_mem(tests.input['memory_MB'], tests.input['execution_time_s'])
    E_network_Ws = calculate_e_network(tests.input['external_data_transfer_MB'], tests.input['internal_data_transfer_MB'])
    E_storage_Ws = calculate_e_storage(tests.input['storage_MB'], tests.input['execution_time_s'])
    M_mgCO2 = calculate_m(tests.input['execution_time_s'])
    SCI = calculate_sci(E_cpu_Ws, E_mem_Ws, M_mgCO2)
    SCI_full = calculate_sci(E_cpu_Ws, E_mem_Ws, M_mgCO2, E_network_Ws, E_storage_Ws)

    # Run tests
    try:
        assert CPU_MIN_W * CPU_MAX_W * CPU_LOAD == tests.constants['CPU'], f"Wrong CPU constants"
    except AssertionError as e:
        print(e)
    try:
        print(f"E_cpu = {E_cpu_Ws} Ws")
        assert E_cpu_Ws== tests.output['E_cpu_Ws'], f"Expected {tests.output['E_cpu_Ws']} but got {E_cpu_Ws}"
        print("Test E_cpu_Ws PASSED")
    except AssertionError as e:
        print("Test E_cpu_Ws FAILED with error: ")
        print(e)
    try:
        assert MEM_COEF == tests.constants['Memory'], f"Wrong Memory constant"
    except AssertionError as e:
        print(e)
    try:
        print(f"E_mem = {E_mem_Ws} Ws")
        assert E_mem_Ws== tests.output['E_mem_Ws'], f"Expected {tests.output['E_mem_Ws']} but got {E_mem_Ws}"
        print("Test E_mem_Ws PASSED")
    except AssertionError as e:
        print("Test E_mem_Ws FAILED with error: ")
        print(e)
    try:
        assert round(TE * EL * RR * TR / 1000000000, 7) == tests.constants['Embodied'], f"Wrong Embodied Emissions constants"
    except AssertionError as e:
        print(e)
    try:
        print(f"M = {M_mgCO2} mgCO2")
        assert M_mgCO2== tests.output['M_mgCO2'], f"Expected {tests.output['M_mgCO2']} but got {M_mgCO2}"
        print("Test M_mgCO2 PASSED")
    except AssertionError as e:
        print("Test M_mgCO2 FAILED with error: ")
        print(e)
    try:
        assert round(I * PUE * 10000000,5) == tests.constants['CarbonIntensityPUE'], f"Wrong Carbon Intensity or PUE constant"
    except AssertionError as e:
        print(e)
    try:
        print(f"SCI = {SCI} mgCO2")
        assert SCI== tests.output['SCI_mgCO2'], f"Expected {tests.output['SCI_mgCO2']} but got {SCI}"
        print("Test SCI_mgCO2 PASSED")
    except AssertionError as e:
        print("Test SCI_mgCO2 FAILED with error: ")
        print(e)
    print("\n")
    print("########## BONUS SECTION ##########")
    print("\n")
    try:
        assert NTW_EXT_COEF == tests.constants['Network'], f"Wrong Network constants"
    except AssertionError as e:
        print(e)
    try:
        print(f"E_network = {E_network_Ws} Ws")
        assert E_network_Ws== tests.output['E_network_Ws'], f"Expected {tests.output['E_network_Ws']} but got {E_network_Ws}"
        print("Test E_network_Ws PASSED")
    except AssertionError as e:
        print("Test E_network_Ws FAILED with error: ")
        print(e)
    try:
        assert round(STORAGE_COEF * REPLICATION_FACTOR, 1) == tests.constants['Storage'], f"Wrong Storage constants"
    except AssertionError as e:
        print(e)
    try:
        print(f"E_storage = {E_storage_Ws} Ws")
        assert E_storage_Ws== tests.output['E_storage_ws'], f"Expected {tests.output['E_storage_ws']} but got {E_storage_Ws}"
        print("Test E_storage_ws PASSED")
    except AssertionError as e:
        print("Test E_storage_ws FAILED with error: ")
        print(e)
    try:
        print(f"SCI full = {SCI_full} mgCO2")
        assert SCI_full== tests.output['SCI_full_mgCO2'], f"Expected {tests.output['SCI_full_mgCO2']} but got {SCI_full}"
        print("Test SCI_full_mgCO2 PASSED")
    except AssertionError as e:
        print("Test SCI_full_mgCO2 FAILED with error: ")
        print(e)

if __name__ == "__main__":
    main()