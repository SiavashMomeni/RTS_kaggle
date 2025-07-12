#!/usr/bin/env python3
"""
CLI interface for running experiments
"""
import argparse
from src.experiments import run_batch_experiments, load_config

def main():
    parser = argparse.ArgumentParser(description='Run scheduling experiments')
    parser.add_argument('--config', type=str, required=True, 
                        help='Path to experiment config file')
    parser.add_argument('--output', type=str, default='results',
                        help='Output directory for results')
    parser.add_argument('--batch_size', type=int, default=10,
                        help='Number of experiments per batch')
    args = parser.parse_args()

    configs = load_config(args.config)
    run_batch_experiments(
        configs, 
        batch_size=args.batch_size,
        output_dir=args.output
    )

if __name__ == "__main__":
    main()
