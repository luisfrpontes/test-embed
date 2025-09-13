"""
Tests for Databricks job functionality

These tests validate the core functionality of the databricks_job.py script
to ensure it works correctly both locally and in Databricks environments.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(__file__))

from databricks_job import (
    create_sample_data,
    process_data,
    generate_summary,
    parse_arguments
)


class TestDataProcessing:
    """Test data processing functions"""
    
    def test_create_sample_data(self):
        """Test sample data creation"""
        # Test default size
        data = create_sample_data()
        assert len(data) == 100
        assert list(data.columns) == ['id', 'value', 'category', 'timestamp']
        
        # Test custom size
        data = create_sample_data(50)
        assert len(data) == 50
        
        # Test data types
        assert data['id'].dtype == 'int64'
        assert data['value'].dtype == 'float64'
        assert data['category'].dtype == 'object'
        assert pd.api.types.is_datetime64_any_dtype(data['timestamp'])
    
    def test_process_data(self):
        """Test data processing function"""
        # Create test data
        test_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [1.0, 2.0, 3.0],
            'category': ['A', 'B', 'A'],
            'timestamp': pd.date_range('2024-01-01', periods=3, freq='1h')
        })
        
        # Process the data
        processed = process_data(test_data.copy())
        
        # Check that new columns were added
        expected_columns = [
            'id', 'value', 'category', 'timestamp', 'processed_at',
            'value_squared', 'value_log', 'value_normalized',
            'category_mean', 'category_std', 'category_count'
        ]
        
        for col in expected_columns:
            assert col in processed.columns, f"Missing column: {col}"
        
        # Check calculated values
        assert processed['value_squared'].iloc[0] == 1.0
        assert processed['value_squared'].iloc[1] == 4.0
        assert processed['value_squared'].iloc[2] == 9.0
        
        # Check that category stats were added
        assert processed['category_count'].iloc[0] == 2  # Category A appears twice
        assert processed['category_count'].iloc[1] == 1  # Category B appears once
    
    def test_generate_summary(self):
        """Test summary generation"""
        test_data = pd.DataFrame({
            'value': [1.0, 2.0, 3.0, 4.0, 5.0],
            'category': ['A', 'B', 'A', 'C', 'B']
        })
        
        summary = generate_summary(test_data, 'test')
        
        # Check summary keys
        expected_keys = [
            'environment', 'total_records', 'categories',
            'avg_value', 'std_value', 'min_value', 'max_value',
            'processing_time', 'null_values'
        ]
        
        for key in expected_keys:
            assert key in summary, f"Missing summary key: {key}"
        
        # Check summary values
        assert summary['environment'] == 'test'
        assert summary['total_records'] == 5
        assert summary['categories'] == 3
        assert summary['avg_value'] == 3.0
        assert summary['min_value'] == 1.0
        assert summary['max_value'] == 5.0
        assert summary['null_values'] == 0


class TestArgumentParsing:
    """Test command line argument parsing"""
    
    @patch('sys.argv', ['databricks_job.py'])
    def test_default_arguments(self):
        """Test default argument values"""
        args = parse_arguments()
        assert args.input_path == '/tmp/input'
        assert args.output_path == '/tmp/output'
        assert args.environment == 'dev'
        assert args.num_records == 100
    
    @patch('sys.argv', [
        'databricks_job.py',
        '--input-path', '/custom/input',
        '--output-path', '/custom/output',
        '--environment', 'prod',
        '--num-records', '200'
    ])
    def test_custom_arguments(self):
        """Test custom argument values"""
        args = parse_arguments()
        assert args.input_path == '/custom/input'
        assert args.output_path == '/custom/output'
        assert args.environment == 'prod'
        assert args.num_records == 200


class TestDataValidation:
    """Test data validation and edge cases"""
    
    def test_empty_dataframe(self):
        """Test processing empty dataframe"""
        empty_df = pd.DataFrame()
        
        # Should handle empty dataframe gracefully
        processed = process_data(empty_df)
        assert len(processed) == 0
        assert 'processed_at' in processed.columns
    
    def test_missing_columns(self):
        """Test processing dataframe with missing expected columns"""
        df_no_value = pd.DataFrame({
            'id': [1, 2, 3],
            'category': ['A', 'B', 'C']
        })
        
        # Should handle missing 'value' column gracefully
        processed = process_data(df_no_value)
        assert len(processed) == 3
        assert 'processed_at' in processed.columns
    
    def test_null_values(self):
        """Test processing data with null values"""
        df_with_nulls = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [1.0, np.nan, 3.0],
            'category': ['A', None, 'C']
        })
        
        processed = process_data(df_with_nulls)
        summary = generate_summary(processed, 'test')
        
        # Should track null values
        assert summary['null_values'] > 0


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__])