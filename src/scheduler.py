import heapq
import time
import torch
from collections import defaultdict
from .core import Bundle, GangTask, Core

class GangScheduler:
    def __init__(self, num_cores, scheduling_policy='FIFO', 
                 allocation_policy='FFD', migration_policy='None'):
        self.num_cores = num_cores
        self.scheduling_policy = scheduling_policy
        self.allocation_policy = allocation_policy
        self.migration_policy = migration_policy
        self.cores = [Core(i) for i in range(num_cores)]
        self.ready_queue = []
        self.running_tasks = []
        self.finished_tasks = []
        self.time = 0
        self.event_queue = []
        self.metrics = {
            'response_times': [],
            'deadline_misses': 0,
            'energy_consumption': 0.0,
            'core_utilization': [0] * num_cores,
            'scheduling_overhead': 0.0,
            'waiting_times': [],
            'migration_count': 0
        }
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # [Include all scheduler methods from previous implementation]
    # add_task, release_task, schedule, allocate_cores, etc.
