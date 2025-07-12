import yaml
import pandas as pd
from tqdm import tqdm
from .scheduler import GangScheduler

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def generate_tasks(num_tasks, utilization, num_bundles_range=(1, 5)):
    # [Implementation from previous code]
    pass

def run_single_experiment(config):
    # [Implementation from previous code]
    pass

def run_batch_experiments(configs, batch_size=10, output_dir=None):
    """Run experiments in batches with checkpointing"""
    results = []
    
    for i in range(0, len(configs), batch_size):
        batch = configs[i:i+batch_size]
        batch_results = []
        
        for config in tqdm(batch, desc=f"Batch {i//batch_size + 1}"):
            try:
                result = run_single_experiment(config)
                batch_results.append(result)
            except Exception as e:
                print(f"Error in config {config}: {str(e)}")
        
        results.extend(batch_results)
        
        # Save checkpoint
        if output_dir:
            checkpoint_df = pd.DataFrame(results)
            checkpoint_df.to_csv(f"{output_dir}/checkpoint_batch_{i//batch_size}.csv", index=False)
    
    return results
