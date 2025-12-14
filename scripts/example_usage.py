"""Example usage of the Data Explorer API."""
import requests
import json


BASE_URL = "http://localhost:8000/api/v1"


def check_health():
    """Check API health."""
    response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
    print("Health Check:")
    print(json.dumps(response.json(), indent=2))
    print()


def list_datasets():
    """List available datasets."""
    response = requests.get(f"{BASE_URL}/query/datasets")
    print("Available Datasets:")
    print(json.dumps(response.json(), indent=2))
    print()
    return response.json()


def get_dataset_info(dataset_name):
    """Get dataset information."""
    response = requests.get(f"{BASE_URL}/query/datasets/{dataset_name}")
    print(f"Dataset Info - {dataset_name}:")
    print(json.dumps(response.json(), indent=2))
    print()


def simple_query():
    """Execute a simple query."""
    query = {
        "dataset": "sales_data",
        "columns": ["product", "region", "revenue"],
        "limit": 5
    }
    
    response = requests.post(f"{BASE_URL}/query/execute", json=query)
    print("Simple Query Results:")
    print(json.dumps(response.json(), indent=2))
    print()


def filtered_query():
    """Execute a query with filters."""
    query = {
        "dataset": "sales_data",
        "columns": ["product", "region", "revenue", "quantity"],
        "filters": [
            {
                "column": "region",
                "operator": "=",
                "value": "North"
            },
            {
                "column": "revenue",
                "operator": ">",
                "value": 1000
            }
        ],
        "order_by": [
            {
                "column": "revenue",
                "direction": "DESC"
            }
        ],
        "limit": 10
    }
    
    response = requests.post(f"{BASE_URL}/query/execute", json=query)
    print("Filtered Query Results:")
    print(json.dumps(response.json(), indent=2))
    print()


def aggregated_query():
    """Execute a query with aggregations."""
    query = {
        "dataset": "sales_data",
        "columns": ["region", "product"],
        "aggregates": [
            {
                "function": "sum",
                "column": "revenue",
                "alias": "total_revenue"
            },
            {
                "function": "avg",
                "column": "quantity",
                "alias": "avg_quantity"
            }
        ],
        "group_by": ["region", "product"],
        "order_by": [
            {
                "column": "total_revenue",
                "direction": "DESC"
            }
        ],
        "limit": 10
    }
    
    response = requests.post(f"{BASE_URL}/query/execute", json=query)
    print("Aggregated Query Results:")
    print(json.dumps(response.json(), indent=2))
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Data Explorer API - Example Usage")
    print("=" * 60)
    print()
    
    try:
        # Check health
        check_health()
        
        # List datasets
        datasets = list_datasets()
        
        # Get dataset info
        if datasets:
            dataset_name = datasets[0]['name']
            get_dataset_info(dataset_name)
        
        # Execute queries
        simple_query()
        filtered_query()
        aggregated_query()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running.")
        print("Start the server with: python run.py")
    except Exception as e:
        print(f"Error: {e}")
