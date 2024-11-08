def calculate_co2_emissions(schedule, carbonIntensity, coreCapacity=None,  embodiedTE=None, ToR=None):
    """
    Calculate CO2 emissions for a given schedule
    
    Args:
        schedule: List of [hour, jobs] pairs for single DC, or list of lists for multiple DCs
        carbonIntensity: List/matrix of carbon intensities
        coreCapacity: List of core capacities per DC (for multi-DC scenario)
    
    Returns:
        Total CO2 emissions in grams
    """
    total_emissions = 0
    # Assume 3W per core when active
    energy_per_job = 3 * (1/60) / 1000  # kWh (1 minute runtime)
    time_in_use = 1   # in minutes
    EL = 4 * 365 * 24 * 60  # 4 years in minutes


    
    # Single datacenter case
    if isinstance(carbonIntensity[0], (int, float)):
        for hour, jobs in schedule:
            operational = energy_per_job * carbonIntensity[hour] # gCO2 / job
            #embodied = (embodiedTE * (time_in_use / EL) * (1 / ToR)) * 1000 # g of CO2
            total_emissions += jobs * operational # gCO2
        return total_emissions / 1000 #kgCo2
    
    # Multiple datacenters case
    for dc_index, dc_schedule in enumerate(schedule):
        for hour, jobs in dc_schedule:
            operational = energy_per_job * carbonIntensity[dc_index][hour] # g of CO2
            embodied = 0
            if embodiedTE: 
                embodied = (embodiedTE[dc_index] * (time_in_use / EL) * (1 / ToR[dc_index])) * 1000 # g of CO2
            total_emissions += jobs * (operational + embodied)
    return total_emissions / 1000 #kgCo2

def calculate_baseline_emissions(jobsNumber, carbonIntensity, coreCapacity=None,  embodiedTE=None, ToR=None):
    """Calculate emissions without carbon-aware optimization (earliest possible scheduling)"""
    if isinstance(carbonIntensity[0], (int, float)):
        # Single DC - fill earliest slots first
        cores_per_hour = 10 * 60  # 10 cores × 60 minutes
        baseline_schedule = []
        jobs_left = jobsNumber
        hour = 0
        
        while jobs_left > 0 and hour < len(carbonIntensity):
            jobs_this_hour = min(cores_per_hour, jobs_left)
            baseline_schedule.append([hour, jobs_this_hour])
            jobs_left -= jobs_this_hour
            hour += 1
            
        return calculate_co2_emissions(baseline_schedule, carbonIntensity,  embodiedTE, ToR)
    
    # Multiple DCs - distribute evenly across DCs in earliest slots
    total_capacity_per_hour = sum(cap * 60 for cap in coreCapacity)
    baseline_schedule = [[] for _ in coreCapacity]
    jobs_left = jobsNumber
    hour = 0
    
    while jobs_left > 0 and hour < len(carbonIntensity[0]):
        # Distribute jobs proportionally to DC capacity
        for dc_index, capacity in enumerate(coreCapacity):
            dc_jobs = min(capacity * 60, int(jobs_left * (capacity * 60 / total_capacity_per_hour)))
            if dc_jobs > 0:
                baseline_schedule[dc_index].append([hour, dc_jobs])
                jobs_left -= dc_jobs
        hour += 1
    
    return calculate_co2_emissions(baseline_schedule, carbonIntensity, coreCapacity)

def compare_emissions(optimized_schedule, jobsNumber, carbonIntensity, coreCapacity=None,  embodiedTE=None, ToR=None):
    """Compare emissions between optimized and baseline schedules"""
    optimized_emissions = calculate_co2_emissions(optimized_schedule, carbonIntensity, coreCapacity,  embodiedTE, ToR)
    baseline_emissions = calculate_baseline_emissions(jobsNumber, carbonIntensity, coreCapacity,  embodiedTE, ToR)
    
    # Calculate theoretical minimum emissions
    if isinstance(carbonIntensity[0], (int, float)):
        sorted_intensities = sorted(carbonIntensity)
        cores_per_hour = 10 * 60
        theoretical_min = 0
        jobs_left = jobsNumber
        idx = 0
        
        while jobs_left > 0 and idx < len(sorted_intensities):
            jobs_this_hour = min(cores_per_hour, jobs_left)
            theoretical_min += jobs_this_hour * (3 * 1/60) * sorted_intensities[idx]
            jobs_left -= jobs_this_hour
            idx += 1
    else:
        # For multiple DCs, use lowest intensity available at each DC
        theoretical_min = float('inf')
        # Complex calculation omitted for brevity - would need to consider DC capacities
        # and optimal distribution across time and location
    
    results = {
        'optimized_emissions': round(optimized_emissions, 2), #kgCO2
        'baseline_emissions': round(baseline_emissions, 2), #kgCO2
        'co2_avoided': round(baseline_emissions - optimized_emissions, 2),
        'theoretical_min': round(theoretical_min, 2) if theoretical_min != float('inf') else None
    }
    
    return results

def print_comparison_results(results):
    '''Format evaluation results with a cyberpunk terminal style'''
    
    # ANSI color codes
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    
    width = 45  # Total width
    
    def create_box_line():
        return f"{DIM}└{'─' * (width-2)}┘{RESET}"
    
    def create_header(text):
        return f"{DIM}┌{'─' * (width-2)}┐{RESET}\n{DIM}│{RESET}{CYAN}{text.center(width-2)}{RESET}{DIM}│{RESET}"
    
    def create_section(text):
        return f"{DIM}├{'─' * (width-2)}┤{RESET}\n{DIM}│{RESET}{YELLOW}{text.center(width-2)}{RESET}{DIM}│{RESET}"
    
    def format_co2(value):
        return f"{abs(value):.2f} kgCO2"
    
    def format_line(label, value, color=GREEN):
        label_part = f"{color}{label}{RESET}"
        value_str = str(value)
        padding = width - len(label) - len(value_str) - 5
        return f"{DIM}│{RESET} {label_part}{' ' * padding}{value_str} {DIM}│{RESET}"
    
    # Calculate reduction percentage
    reduction_percent = (results['co2_avoided'] / results['baseline_emissions'] * 100)
    
    # Build the output
    output = [
        create_header("CARBON EMISSIONS ANALYSIS"),
        create_section("CURRENT EMISSIONS STATUS"),
        format_line("✈  With optimization:      ", format_co2(results['optimized_emissions']), GREEN),
        format_line("🏭 Without optimization:", format_co2(results['baseline_emissions']), RED),
        format_line("📊 Reduction achieved:", f"{reduction_percent:.1f}%", GREEN),
        create_section("CARBON SAVINGS ANALYSIS"),
        format_line("🌍 CO2 avoided:", format_co2(results['co2_avoided']), CYAN)
    ]
    
    # Add theoretical minimum analysis if available
    if results['theoretical_min'] is not None:
        potential_savings = results['optimized_emissions'] - results['theoretical_min']
        if potential_savings <= 0:
            output.append(format_line("✨ Status:", "Perfect optimization!", GREEN))
        else:
            output.append(format_line("📈 Additional savings:", format_co2(potential_savings), YELLOW))
    
    # Add bottom border
    output.append(create_box_line())
    
    # Print the formatted output
    print("\n".join(output))

def print_schedule_comparison(student_schedule, expected_schedule):
    '''Format schedule comparison with a cyberpunk terminal style'''
    width = 45  # Total width for schedule display

    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    
    def create_box_line():
        return f"{DIM}└{'─' * (width-2)}┘{RESET}"
    
    def create_header(text):
        return f"{DIM}┌{'─' * (width-2)}┐{RESET}\n{DIM}│{RESET}{CYAN}{text.center(width-2)}{RESET}{DIM}│{RESET}"
    
    def create_section(text):
        return f"{DIM}├{'─' * (width-2)}┤{RESET}\n{DIM}│{RESET}{YELLOW}{text.center(width-2)}{RESET}{DIM}│{RESET}"
    
    def format_schedule_line(dc_num, schedule, color):
        schedule_str = " ".join([f"[{hour}:{jobs}]" for hour, jobs in schedule])
        label = f"DC{dc_num}"
        content = f"{color}{label:<4} {schedule_str}{RESET}"
        padding = width - len(label) - len(schedule_str) - 5
        return f"{DIM}│{RESET} {content}{' ' * padding} {DIM}│{RESET}"

    output = [
        create_header("SCHEDULING ANALYSIS"),
        create_section("YOUR SCHEDULE")
    ]
    
    for dc_idx, dc_schedule in enumerate(student_schedule):
        output.append(format_schedule_line(dc_idx + 1, dc_schedule, GREEN))
    
    output.extend([
        create_section("EXPECTED SCHEDULE")
    ])
    
    for dc_idx, dc_schedule in enumerate(expected_schedule):
        output.append(format_schedule_line(dc_idx + 1, dc_schedule, CYAN))
    
    is_matching = student_schedule == expected_schedule
    status_color = GREEN if is_matching else RED
    status_text = '✓ Schedules Match' if is_matching else '✗ Schedules Differ'
    output.extend([
        create_section("VALIDATION RESULT"),
        f"{DIM}│{RESET} {status_color}{status_text:^{width-4}}{RESET} {DIM}│{RESET}",
        create_box_line()
    ])
    
    print("\n".join(output)) 