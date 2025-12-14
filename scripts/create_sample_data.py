"""Sample script to create test Parquet data."""
import pandas as pd
import numpy as np
from pathlib import Path


def create_sample_sales_data():
    """Create sample sales dataset."""
    np.random.seed(42)
    
    # Generate sample data
    n_records = 1000
    
    data = {
        'order_id': range(1, n_records + 1),
        'product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'], n_records),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
        'revenue': np.random.uniform(100, 2000, n_records).round(2),
        'quantity': np.random.randint(1, 10, n_records),
        'customer_id': np.random.randint(1, 200, n_records),
        'order_date': pd.date_range('2023-01-01', periods=n_records, freq='H'),
    }
    
    df = pd.DataFrame(data)
    
    # Save to parquet
    output_dir = Path(__file__).parent.parent / 'data' / 'sample'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / 'sales_data.parquet'
    df.to_parquet(output_path, index=False)
    
    print(f"Created sample sales data: {output_path}")
    print(f"Records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nSample data:")
    print(df.head())


def create_sample_customer_data():
    """Create sample customer dataset."""
    np.random.seed(42)
    
    n_customers = 200
    
    data = {
        'customer_id': range(1, n_customers + 1),
        'customer_name': [f'Customer {i}' for i in range(1, n_customers + 1)],
        'email': [f'customer{i}@example.com' for i in range(1, n_customers + 1)],
        'segment': np.random.choice(['Enterprise', 'SMB', 'Individual'], n_customers),
        'country': np.random.choice(['USA', 'UK', 'Canada', 'Germany', 'France'], n_customers),
        'join_date': pd.date_range('2020-01-01', periods=n_customers, freq='D'),
    }
    
    df = pd.DataFrame(data)
    
    output_dir = Path(__file__).parent.parent / 'data' / 'sample'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / 'customer_data.parquet'
    df.to_parquet(output_path, index=False)
    
    print(f"\nCreated sample customer data: {output_path}")
    print(f"Records: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nSample data:")
    print(df.head())


if __name__ == "__main__":
    print("Creating sample datasets...")
    create_sample_sales_data()
    create_sample_customer_data()
    print("\nSample datasets created successfully!")
