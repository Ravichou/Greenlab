# We will use this file to define the input and output of the tests
input = {
    "execution_time_s": 10,
    "cpu_time_s": 8,
    "cores_requested": 2,
    "memory_MB": 50,
    "internal_data_transfer_MB": 50,
    "external_data_transfer_MB": 20,
    "storage_MB": 2000
    }

output = {
    "E_cpu_Ws": 36.32,
    "E_mem_Ws": 0.196,
    "M_mgCO2": 12.433,
    "SCI_mgCO2": 16.38,
    "E_network_Ws": 72.0,
    "E_storage_ws": 0.072,
    "SCI_full_mgCO2": 24.17
    }

constants = {
    "CPU": 1.4664,
    "Memory": 0.392,
    "Embodied": 5071.4325504,
    "Network": 0.001,
    "Storage": 3.6,
    "CarbonIntensityPUE": 1.08098
    }