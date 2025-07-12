import numpy as np
import random

class Bundle:
    def __init__(self, num_cores, wcet):
        self.num_cores = num_cores
        self.wcet = wcet
        self.remaining = wcet
        self.start_time = -1

class GangTask:
    def __init__(self, task_id, period, wcet_total, num_bundles, criticality=1):
        self.id = task_id
        self.period = period
        self.deadline = period
        self.release_time = 0
        self.bundles = []
        self.bundle_index = 0
        self.finish_time = None
        self.response_time = None
        self.missed_deadline = False
        self.assigned_cores = []
        
        # Generate bundles with variable core requirements
        bundle_wcets = np.random.dirichlet(np.ones(num_bundles)) * wcet_total
        for i in range(num_bundles):
            cores = random.randint(1, 8)
            self.bundles.append(Bundle(cores, bundle_wcets[i]))
    
    def __lt__(self, other):
        return self.id < other.id
    
    def current_bundle(self):
        if self.bundle_index < len(self.bundles):
            return self.bundles[self.bundle_index]
        return None
    
    def advance_bundle(self):
        self.bundle_index += 1
        return self.current_bundle() is not None
    
    def total_workload(self):
        return sum(b.wcet for b in self.bundles)
    
    def max_cores_required(self):
        return max(b.num_cores for b in self.bundles)

class Core:
    def __init__(self, core_id, speed=1.0):
        self.id = core_id
        self.speed = speed
        self.task = None
        self.idle = True
        self.utilization = 0
        self.energy_consumed = 0
    
    def execute(self, duration):
        if self.task:
            self.utilization += duration
            self.energy_consumed += duration * 0.2
    
    def reset(self):
        self.task = None
        self.idle = True
        self.utilization = 0
        self.energy_consumed = 0
