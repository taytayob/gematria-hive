#!/usr/bin/env python3
"""
Run Autonomous Agent

Purpose: Main script to run the autonomous agent with configurable settings

Usage:
    python run_autonomous.py [--max-commits N] [--max-time HOURS] [--max-tasks N] 
                              [--auto-push] [--config CONFIG_FILE]

Author: Gematria Hive Team
Date: January 6, 2025
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add agents to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.autonomous import AutonomousAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def load_config(config_file: str) -> dict:
    """
    Load configuration from JSON file
    
    Args:
        config_file: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logger.info(f"Loaded configuration from {config_file}")
        return config
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        return {}


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Run autonomous agent for committing and working autonomously'
    )
    
    parser.add_argument(
        '--max-commits',
        type=int,
        default=10,
        help='Maximum number of commits before stopping (default: 10)'
    )
    
    parser.add_argument(
        '--max-time',
        type=float,
        default=8.0,
        help='Maximum hours to run before stopping (default: 8.0)'
    )
    
    parser.add_argument(
        '--max-tasks',
        type=int,
        default=50,
        help='Maximum number of tasks to process before stopping (default: 50)'
    )
    
    parser.add_argument(
        '--commit-interval',
        type=int,
        default=300,
        help='Minimum seconds between commits (default: 300 = 5 minutes)'
    )
    
    parser.add_argument(
        '--auto-push',
        action='store_true',
        help='Automatically push commits to remote'
    )
    
    parser.add_argument(
        '--branch',
        type=str,
        default=None,
        help='Git branch to work on (default: current branch)'
    )
    
    parser.add_argument(
        '--work-dir',
        type=str,
        default=None,
        help='Working directory (default: current directory)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to JSON configuration file'
    )
    
    parser.add_argument(
        '--tasks',
        type=str,
        default=None,
        help='Path to JSON file with tasks to process'
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = {}
    if args.config:
        config = load_config(args.config)
    
    # Override config with command-line arguments
    settings = {
        'max_commits': args.max_commits or config.get('max_commits', 10),
        'max_time_hours': args.max_time or config.get('max_time_hours', 8.0),
        'max_tasks': args.max_tasks or config.get('max_tasks', 50),
        'commit_interval_seconds': args.commit_interval or config.get('commit_interval_seconds', 300),
        'auto_push': args.auto_push or config.get('auto_push', False),
        'branch': args.branch or config.get('branch'),
        'work_dir': args.work_dir or config.get('work_dir')
    }
    
    logger.info("=" * 60)
    logger.info("Starting Autonomous Agent")
    logger.info("=" * 60)
    logger.info(f"Settings:")
    for key, value in settings.items():
        logger.info(f"  {key}: {value}")
    logger.info("=" * 60)
    
    # Load tasks if provided
    tasks = None
    if args.tasks:
        try:
            with open(args.tasks, 'r') as f:
                tasks = json.load(f)
            logger.info(f"Loaded {len(tasks)} tasks from {args.tasks}")
        except Exception as e:
            logger.error(f"Error loading tasks file: {e}")
            tasks = None
    
    # Create and run agent
    try:
        agent = AutonomousAgent(**settings)
        
        # Run the agent
        summary = agent.run(tasks=tasks)
        
        # Save log
        log_file = agent.save_log()
        
        # Print summary
        logger.info("=" * 60)
        logger.info("Autonomous Agent Run Summary")
        logger.info("=" * 60)
        logger.info(f"Start Time: {summary['start_time']}")
        logger.info(f"End Time: {summary['end_time']}")
        logger.info(f"Elapsed Time: {summary['elapsed_hours']:.2f} hours")
        logger.info(f"Commits Made: {summary['commits_made']}")
        logger.info(f"Tasks Processed: {summary['tasks_processed']}")
        logger.info(f"Activity Log: {log_file}")
        logger.info("=" * 60)
        
        # Check milestones
        milestones = summary['milestones_reached']
        if milestones['reached']:
            reasons = []
            if milestones['max_commits']:
                reasons.append(f"Max commits reached ({milestones['commit_count']})")
            if milestones['max_time']:
                reasons.append(f"Max time reached ({milestones['elapsed_hours']:.2f}h)")
            if milestones['max_tasks']:
                reasons.append(f"Max tasks reached ({milestones['task_count']})")
            logger.info(f"Stopped due to: {', '.join(reasons)}")
        
        logger.info("Autonomous agent run completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Stopping...")
        if 'agent' in locals():
            agent.commit_changes()  # Final commit before stopping
            agent.save_log()
    except Exception as e:
        logger.error(f"Error running autonomous agent: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

