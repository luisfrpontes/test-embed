#!/usr/bin/env python3
"""
Example usage script for the Databricks test-embed repository

This script demonstrates how to use the databricks_job.py module
and provides examples for different use cases.
"""

import sys
import os
from pathlib import Path

# Add current directory to path to import our module
sys.path.insert(0, str(Path(__file__).parent))

from databricks_job import (
    create_sample_data,
    process_data,
    generate_summary,
    setup_logging
)


def example_basic_usage():
    """Example of basic data processing"""
    print("=== Basic Usage Example ===")
    
    # Create sample data
    data = create_sample_data(50)
    print(f"Created sample data with {len(data)} records")
    
    # Process the data
    processed = process_data(data)
    print(f"Processed data shape: {processed.shape}")
    
    # Generate summary
    summary = generate_summary(processed, 'example')
    print("Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    return processed


def example_custom_data():
    """Example with custom data structure"""
    print("\n=== Custom Data Example ===")
    
    import pandas as pd
    import numpy as np
    
    # Create custom data
    custom_data = pd.DataFrame({
        'product_id': range(1, 21),
        'value': np.random.uniform(10, 100, 20),
        'category': np.random.choice(['Electronics', 'Books', 'Clothing'], 20),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 20)
    })
    
    print(f"Custom data shape: {custom_data.shape}")
    print(custom_data.head())
    
    # Process custom data
    processed = process_data(custom_data)
    print(f"\nProcessed custom data shape: {processed.shape}")
    
    return processed


def example_error_handling():
    """Example of error handling with edge cases"""
    print("\n=== Error Handling Example ===")
    
    import pandas as pd
    import numpy as np
    
    # Empty dataframe
    empty_df = pd.DataFrame()
    processed_empty = process_data(empty_df)
    print(f"Empty dataframe result: {len(processed_empty)} records")
    
    # Dataframe with missing columns
    incomplete_df = pd.DataFrame({
        'id': [1, 2, 3],
        'other_column': ['A', 'B', 'C']
    })
    processed_incomplete = process_data(incomplete_df)
    print(f"Incomplete dataframe result: {processed_incomplete.shape}")
    
    # Dataframe with null values
    null_df = pd.DataFrame({
        'value': [1.0, np.nan, 3.0, None, 5.0],
        'category': ['A', 'B', None, 'C', 'A']
    })
    processed_null = process_data(null_df)
    summary_null = generate_summary(processed_null, 'null_test')
    print(f"Null values handled: {summary_null['null_values']} nulls detected")


def example_environment_simulation():
    """Example simulating different environments"""
    print("\n=== Environment Simulation Example ===")
    
    environments = ['dev', 'staging', 'prod']
    record_counts = [10, 100, 1000]
    
    for env, count in zip(environments, record_counts):
        print(f"\nSimulating {env} environment with {count} records:")
        
        data = create_sample_data(count)
        processed = process_data(data)
        summary = generate_summary(processed, env)
        
        print(f"  Records: {summary['total_records']}")
        print(f"  Categories: {summary['categories']}")
        print(f"  Avg Value: {summary['avg_value']:.4f}")


def main():
    """Main demonstration function"""
    print("Databricks Test-Embed Repository Examples")
    print("=" * 50)
    
    # Set up logging
    logger = setup_logging()
    logger.info("Starting examples")
    
    try:
        # Run examples
        example_basic_usage()
        example_custom_data()
        example_error_handling()
        example_environment_simulation()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise


if __name__ == "__main__":
    main()