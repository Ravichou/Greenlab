def reportPerformances(cpu_load, 
                       self_cpu_time, 
                       self_ram_MB,
                       self_sci,
                       child_cpu_time,
                       child_ram_MB,
                       child_sci):
    print("------------------------", end="")
    print("--- Host metrics ---", end="")
    print("------------------------")
    print("CPU load in percent : " + str(cpu_load))
    print("-----------------------", end="")
    print("--- Runner metrics ---", end="")
    print("-----------------------")
    print("CPU time : " + str(round(self_cpu_time,3) * 1000) + " ms")
    print("RAM usage in MB : " + str(round(self_ram_MB,3)))
    print("SCI score in mgCO2 : " + str(self_sci))
    print("---------------------", end="")
    print("--- Algo performances ---", end="")
    print("----------------------")
    print("CPU time : " + str(round(child_cpu_time, 3) * 1000) + " ms")
    print("RAM in MB : " + str(round(child_ram_MB,3)))
    print("SCI score in mgCO2 : " + str(child_sci))
