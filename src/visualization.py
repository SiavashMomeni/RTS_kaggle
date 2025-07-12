import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

def set_plot_style():
    """Set consistent plotting style"""
    sns.set_style("whitegrid")
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'

def plot_response_time_comparison(results_df, output_dir):
    """Plot response time comparison for different policies"""
    set_plot_style()
    
    # Create a grid of subplots: cores vs tasks
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for i, cores in enumerate([4, 8, 16, 32]):
        ax = axes[i]
        subset = results_df[results_df['cores'] == cores]
        
        for policy in ['FIFO', 'LDF', 'HEFT']:
            policy_data = subset[subset['policy'] == policy]
            if not policy_data.empty:
                ax.plot(policy_data['num_tasks'], policy_data['avg_response'], 
                         'o-', label=policy, linewidth=2.5)
        
        ax.set_title(f'{cores} Cores', fontweight='bold')
        ax.set_xlabel('Number of Tasks')
        ax.set_ylabel('Average Response Time (ms)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.suptitle('Response Time Comparison Across Configurations', fontsize=18, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'response_time_comparison.png'))
    plt.close()

def plot_deadline_success_rate(results_df, output_dir):
    """Plot deadline success rate comparison"""
    set_plot_style()
    
    plt.figure(figsize=(14, 8))
    
    # Create pivot table for success rates
    pivot_table = results_df.pivot_table(
        values='success_rate',
        index='num_tasks',
        columns=['cores', 'policy'],
        aggfunc='mean'
    ).fillna(0) * 100  # Convert to percentage
    
    # Plot each configuration
    for (cores, policy), success_rates in pivot_table.items():
        if policy == 'HEFT':  # Highlight HEFT policy
            plt.plot(success_rates.index, success_rates.values, 
                     'o-', linewidth=3, label=f'{policy} ({cores} cores)')
        else:
            plt.plot(success_rates.index, success_rates.values, 
                     '--', alpha=0.7, label=f'{policy} ({cores} cores)')
    
    plt.title('Deadline Success Rate by Task Count and Policy', fontweight='bold')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Success Rate (%)')
    plt.legend(ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.ylim(0, 100)
    plt.savefig(os.path.join(output_dir, 'deadline_success_rate.png'))
    plt.close()

def plot_energy_utilization(results_df, output_dir):
    """Plot energy consumption vs utilization"""
    set_plot_style()
    
    # Filter for 100 tasks
    subset = results_df[results_df['num_tasks'] == 100]
    
    # Create a grid of subplots: cores vs policies
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    policies = ['FIFO', 'LDF', 'HEFT']
    
    for i, cores in enumerate([4, 8, 16, 32]):
        ax = axes[i]
        core_data = subset[subset['cores'] == cores]
        
        for policy in policies:
            policy_data = core_data[core_data['policy'] == policy]
            if not policy_data.empty:
                ax.plot(policy_data['utilization'], policy_data['energy'], 
                         's-', label=policy, linewidth=2.5)
        
        ax.set_title(f'{cores} Cores', fontweight='bold')
        ax.set_xlabel('Utilization')
        ax.set_ylabel('Energy Consumption (J)')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
    
    plt.suptitle('Energy Consumption vs Utilization (100 Tasks)', 
                 fontsize=18, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'energy_utilization.png'))
    plt.close()

def plot_scheduling_overhead(results_df, output_dir):
    """Plot scheduling overhead comparison"""
    set_plot_style()
    
    plt.figure(figsize=(14, 8))
    
    # Group by task count and policy
    grouped = results_df.groupby(['num_tasks', 'policy'])['overhead'].mean().reset_index()
    
    for policy in ['FIFO', 'LDF', 'HEFT']:
        policy_data = grouped[grouped['policy'] == policy]
        plt.plot(policy_data['num_tasks'], policy_data['overhead'], 
                 'o-', label=policy, linewidth=2.5)
    
    plt.title('Scheduling Overhead by Task Count', fontweight='bold')
    plt.xlabel('Number of Tasks')
    plt.ylabel('Overhead (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.yscale('log')  # Use log scale for better visualization
    plt.savefig(os.path.join(output_dir, 'scheduling_overhead.png'))
    plt.close()

def plot_analysis_comparison(analysis_df, output_dir):
    """Compare analysis methods with simulation results"""
    set_plot_style()
    
    plt.figure(figsize=(14, 8))
    
    # Plot each method
    for method in ['closed_form', 'milp', 'simulation']:
        plt.plot(analysis_df['cores'], analysis_df[method], 'o-', label=method, linewidth=2.5)
    
    plt.title('Response Time Analysis Methods Comparison', fontweight='bold')
    plt.xlabel('Number of Cores')
    plt.ylabel('Average Response Time (ms)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(output_dir, 'analysis_methods_comparison.png'))
    plt.close()

def plot_all_results(results_df, analysis_df, output_dir):
    """Generate all plots and save to output directory"""
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating response time comparison plot...")
    plot_response_time_comparison(results_df, output_dir)
    
    print("Generating deadline success rate plot...")
    plot_deadline_success_rate(results_df, output_dir)
    
    print("Generating energy utilization plot...")
    plot_energy_utilization(results_df, output_dir)
    
    print("Generating scheduling overhead plot...")
    plot_scheduling_overhead(results_df, output_dir)
    
    print("Generating analysis methods comparison plot...")
    plot_analysis_comparison(analysis_df, output_dir)
    
    print("All visualizations saved to", output_dir)
