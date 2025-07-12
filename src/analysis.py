import numpy as np
from scipy.optimize import linprog
import pulp
import time

def closed_form_analysis(tasks, num_cores):
    """
    Closed-form analysis for gang task response times
    Based on the interference model for parallel tasks
    """
    response_times = []
    
    for i, task in enumerate(tasks):
        # Task's total execution demand
        C_i = task.total_workload()
        
        # Interference from higher-priority tasks
        interference = 0
        for j, other_task in enumerate(tasks):
            if i == j:
                continue
                
            # Resource contention factor
            alpha = min(other_task.max_cores_required(), num_cores) / num_cores
            W_j = other_task.total_workload()
            T_j = other_task.period
            
            # Interference contribution
            interference += alpha * (np.ceil(C_i / T_j) * W_j)
        
        # Response time calculation
        R_i = C_i + interference
        response_times.append(R_i)
    
    return response_times

def milp_analysis(tasks, num_cores, time_limit=30):
    """
    MILP-based response time analysis using PuLP
    Models task scheduling as an optimization problem
    """
    try:
        # Create the MILP problem
        prob = pulp.LpProblem("Gang_Task_Response_Time_Analysis", pulp.LpMinimize)
        
        # Create variables
        R = {}  # Response time for each task
        for i, task in enumerate(tasks):
            R[i] = pulp.LpVariable(f"R_{i}", lowBound=task.total_workload(), cat='Continuous')
        
        # Objective: Minimize maximum response time
        R_max = pulp.LpVariable("R_max", lowBound=0, cat='Continuous')
        prob += R_max
        
        # Constraints
        for i, task in enumerate(tasks):
            C_i = task.total_workload()
            T_i = task.period
            
            # R_max must be at least each response time
            prob += R_max >= R[i]
            
            # Response time must include execution and interference
            interference = 0
            for j, other_task in enumerate(tasks):
                if i == j:
                    continue
                
                C_j = other_task.total_workload()
                T_j = other_task.period
                alpha = min(other_task.max_cores_required(), num_cores) / num_cores
                
                # Interference constraint
                prob += R[i] >= C_i + alpha * pulp.lpSum(
                    (C_j) * (R[i] // T_j)
                )
            
            # Deadline constraint
            prob += R[i] <= T_i
    
        # Solve with time limit
        prob.solve(pulp.PULP_CBC_CMD(timeLimit=time_limit, msg=False))
        
        # Extract results
        if pulp.LpStatus[prob.status] == "Optimal":
            return [pulp.value(R[i]) for i in range(len(tasks))]
        else:
            print(f"MILP optimization failed with status: {pulp.LpStatus[prob.status]}")
            return closed_form_analysis(tasks, num_cores)
            
    except Exception as e:
        print(f"Error in MILP analysis: {str(e)}")
        return closed_form_analysis(tasks, num_cores)

def compare_analysis_methods(tasks, num_cores):
    """Compare different analysis methods and return metrics"""
    results = {}
    
    # Closed-form analysis
    start_time = time.time()
    cf_results = closed_form_analysis(tasks, num_cores)
    cf_time = time.time() - start_time
    results['closed_form'] = {
        'response_times': cf_results,
        'avg_response': np.mean(cf_results),
        'max_response': np.max(cf_results),
        'execution_time': cf_time
    }
    
    # MILP analysis
    start_time = time.time()
    milp_results = milp_analysis(tasks, num_cores)
    milp_time = time.time() - start_time
    results['milp'] = {
        'response_times': milp_results,
        'avg_response': np.mean(milp_results),
        'max_response': np.max(milp_results),
        'execution_time': milp_time
    }
    
    return results
