#!/usr/bin/env python3
"""
Sample Databricks Job Script

This script demonstrates a simple data processing workflow that can be 
embedded in Databricks jobs. It's a Python version of the Jupyter notebook
for environments where script execution is preferred.
"""

import pandas as pd
import numpy as np
import argparse
import sys
from datetime import datetime
from pathlib import Path


def setup_logging():
    """Set up basic logging for the job"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Sample Databricks data processing job')
    parser.add_argument('--input-path', default='/tmp/input', 
                       help='Input data path')
    parser.add_argument('--output-path', default='/tmp/output', 
                       help='Output data path')
    parser.add_argument('--environment', default='dev', 
                       choices=['dev', 'staging', 'prod'],
                       help='Environment (dev/staging/prod)')
    parser.add_argument('--num-records', type=int, default=100,
                       help='Number of sample records to generate')
    
    return parser.parse_args()


def get_databricks_widgets():
    """Get parameters from Databricks widgets if available"""
    try:
        # These will work in Databricks environment
        input_path = dbutils.widgets.get("input_path")
        output_path = dbutils.widgets.get("output_path") 
        environment = dbutils.widgets.get("environment")
        num_records = int(dbutils.widgets.get("num_records"))
        
        return input_path, output_path, environment, num_records
    except:
        # Not in Databricks environment
        return None, None, None, None


def create_sample_data(num_records=100):
    """Create sample data for processing"""
    logger = setup_logging()
    logger.info(f"Creating sample data with {num_records} records")
    
    data = pd.DataFrame({
        'id': range(1, num_records + 1),
        'value': np.random.randn(num_records),
        'category': np.random.choice(['A', 'B', 'C'], num_records),
        'timestamp': pd.date_range('2024-01-01', periods=num_records, freq='1h')
    })
    
    return data


def process_data(data):
    """
    Main data processing function
    
    Args:
        data (pd.DataFrame): Input data to process
        
    Returns:
        pd.DataFrame: Processed data
    """
    logger = setup_logging()
    logger.info(f"Processing {len(data)} records")
    
    # Handle empty dataframe
    if len(data) == 0:
        logger.info("Empty dataframe provided, returning empty dataframe with processed_at column")
        empty_result = data.copy()
        empty_result['processed_at'] = datetime.now()
        return empty_result
    
    # Add processing timestamp
    data['processed_at'] = datetime.now()
    
    # Add calculated fields only if 'value' column exists
    if 'value' in data.columns:
        data['value_squared'] = data['value'] ** 2
        data['value_log'] = np.log1p(data['value'].abs())
        
        # Only calculate normalized values if we have more than one record
        if len(data) > 1 and data['value'].std() != 0:
            data['value_normalized'] = (data['value'] - data['value'].mean()) / data['value'].std()
        else:
            data['value_normalized'] = 0.0
    
    # Add category statistics only if both 'category' and 'value' columns exist
    if 'category' in data.columns and 'value' in data.columns:
        try:
            category_stats = data.groupby('category')['value'].agg(['mean', 'std', 'count']).reset_index()
            category_stats.columns = ['category', 'category_mean', 'category_std', 'category_count']
            data = data.merge(category_stats, on='category', how='left')
        except Exception as e:
            logger.warning(f"Could not compute category statistics: {e}")
    
    logger.info(f"Processing completed. Output shape: {data.shape}")
    return data


def save_data(data, output_path, environment):
    """
    Save processed data to output location
    
    Args:
        data (pd.DataFrame): Data to save
        output_path (str): Output path
        environment (str): Environment name
    """
    logger = setup_logging()
    
    try:
        # Try Databricks/Spark approach first
        spark_df = spark.createDataFrame(data)
        
        # Save as parquet for efficient storage
        parquet_path = f"{output_path}/processed_data_{environment}.parquet"
        spark_df.write.mode("overwrite").parquet(parquet_path)
        logger.info(f"Data saved as Spark DataFrame to {parquet_path}")
        
        # Also save CSV for easy viewing
        csv_path = f"{output_path}/processed_data_{environment}.csv"
        data.to_csv(csv_path, index=False)
        logger.info(f"Data saved as CSV to {csv_path}")
        
    except:
        # Fallback for local testing
        output_file = f"processed_data_{environment}_local.csv"
        data.to_csv(output_file, index=False)
        logger.info(f"Data saved locally to {output_file}")


def generate_summary(data, environment):
    """Generate processing summary"""
    summary = {
        'environment': environment,
        'total_records': len(data),
        'categories': data['category'].nunique(),
        'avg_value': data['value'].mean(),
        'std_value': data['value'].std(),
        'min_value': data['value'].min(),
        'max_value': data['value'].max(),
        'processing_time': datetime.now().isoformat(),
        'null_values': data.isnull().sum().sum()
    }
    
    return summary


def main():
    """Main execution function"""
    logger = setup_logging()
    logger.info("Starting Databricks job execution")
    
    # Get configuration from Databricks widgets or command line
    widget_input, widget_output, widget_env, widget_records = get_databricks_widgets()
    
    if widget_input:
        # Running in Databricks
        input_path = widget_input
        output_path = widget_output
        environment = widget_env
        num_records = widget_records
        logger.info("Using Databricks widget parameters")
    else:
        # Running locally or with command line args
        args = parse_arguments()
        input_path = args.input_path
        output_path = args.output_path
        environment = args.environment
        num_records = args.num_records
        logger.info("Using command line parameters")
    
    logger.info(f"Configuration:")
    logger.info(f"  Input Path: {input_path}")
    logger.info(f"  Output Path: {output_path}")
    logger.info(f"  Environment: {environment}")
    logger.info(f"  Number of Records: {num_records}")
    
    try:
        # Create sample data (in real scenario, this would load from input_path)
        data = create_sample_data(num_records)
        
        # Process the data
        processed_data = process_data(data)
        
        # Save results
        save_data(processed_data, output_path, environment)
        
        # Generate and display summary
        summary = generate_summary(processed_data, environment)
        
        logger.info("Processing Summary:")
        for key, value in summary.items():
            logger.info(f"  {key}: {value}")
        
        logger.info("Job completed successfully!")
        
        return summary
        
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    summary = main()
    print(f"\nFinal Summary: {summary}")