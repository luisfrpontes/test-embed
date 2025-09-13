# Databricks Test Embed Repository

Repositório para plugar um notebook em job do Databricks e testarmos / Repository to plug a notebook into Databricks jobs and test it.

## Overview

This repository provides a complete setup for integrating Jupyter notebooks and Python scripts with Databricks jobs. It includes sample code, configuration files, and testing infrastructure to help you quickly deploy data processing workflows to Databricks.

## Files Structure

```
├── sample_notebook.ipynb      # Jupyter notebook for Databricks
├── databricks_job.py         # Python script version
├── test_databricks_job.py    # Unit tests
├── requirements.txt          # Python dependencies
├── databricks_config.ini     # Environment configurations
├── job_config.json          # Databricks job definitions
└── README.md                # This file
```

## Features

- **Jupyter Notebook**: Ready-to-use notebook with Databricks widgets support
- **Python Script**: Command-line version for job execution
- **Multiple Environments**: Configuration for dev/staging/prod
- **Testing**: Comprehensive unit tests
- **Documentation**: Complete setup and usage instructions

## Quick Start

### 1. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Python script locally
python databricks_job.py --environment dev --num-records 50

# Run tests
python -m pytest test_databricks_job.py -v
```

### 2. Databricks Setup

1. **Upload Files to Databricks:**
   - Upload `sample_notebook.ipynb` to your Databricks workspace
   - Upload `databricks_job.py` to your workspace or repository

2. **Create a Notebook Job:**
   ```json
   {
     "name": "Sample Processing Job",
     "notebook_task": {
       "notebook_path": "/path/to/sample_notebook",
       "base_parameters": {
         "input_path": "/your/input/path",
         "output_path": "/your/output/path",
         "environment": "dev"
       }
     }
   }
   ```

3. **Create a Python Script Job:**
   ```json
   {
     "name": "Python Script Job", 
     "spark_python_task": {
       "python_file": "/path/to/databricks_job.py",
       "parameters": ["--environment", "dev"]
     }
   }
   ```

## Configuration

### Environment Variables

The code supports configuration through:

- **Databricks Widgets** (when running in notebooks)
- **Command Line Arguments** (when running scripts)
- **Configuration Files** (databricks_config.ini)

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input_path` | Input data location | `/tmp/input` |
| `output_path` | Output data location | `/tmp/output` |
| `environment` | Environment name | `dev` |
| `num_records` | Number of sample records | `100` |

## Notebook Features

The Jupyter notebook (`sample_notebook.ipynb`) includes:

- **Databricks Widgets**: For parameter passing from jobs
- **Data Processing**: Sample ETL pipeline
- **Error Handling**: Graceful fallbacks for local testing
- **Spark Integration**: Native Spark DataFrame operations
- **Logging**: Comprehensive logging and status reporting

## Python Script Features

The Python script (`databricks_job.py`) includes:

- **Command Line Interface**: Full argument parsing
- **Logging**: Structured logging with timestamps
- **Error Handling**: Robust error handling and recovery
- **Data Processing**: Same logic as notebook in script form
- **Flexible I/O**: Supports both local and Databricks storage

## Testing

Run the test suite to validate functionality:

```bash
# Run all tests
python -m pytest test_databricks_job.py -v

# Run specific test
python -m pytest test_databricks_job.py::TestDataProcessing::test_create_sample_data -v

# Run with coverage
python -m pytest test_databricks_job.py --cov=databricks_job --cov-report=html
```

## Databricks Job Configuration

### Using the Job Config File

The `job_config.json` file contains complete job definitions that can be used with the Databricks Jobs API:

```bash
# Create job using Databricks CLI
databricks jobs create --json-file job_config.json

# Or use the REST API
curl -X POST https://your-workspace.cloud.databricks.com/api/2.1/jobs/create \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d @job_config.json
```

### Environment-Specific Deployment

1. **Development**: Use FileStore for quick testing
2. **Staging**: Use mounted storage with validation
3. **Production**: Use optimized clusters and monitoring

## Best Practices

1. **Parameter Management**: Use Databricks widgets for notebook parameters
2. **Error Handling**: Implement comprehensive error handling and logging
3. **Testing**: Test locally before deploying to Databricks
4. **Monitoring**: Set up email notifications for job failures
5. **Resource Management**: Use appropriate cluster sizes for your workload

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed on the cluster
2. **Path Issues**: Verify file paths exist and are accessible
3. **Permission Errors**: Check cluster and storage permissions

### Debugging

1. **Local Testing**: Run scripts locally first
2. **Databricks Logs**: Check cluster logs for detailed error messages
3. **Unit Tests**: Run tests to isolate issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details
