"""
CSV Handler utility for reading and writing metro system data.
"""
import csv
import os
from typing import List, Dict, Any


class CSVHandler:
    """Handles CSV file operations for the metro system."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize CSV handler with data directory path."""
        self.data_dir = data_dir
    
    def read_csv(self, filename: str) -> List[Dict[str, Any]]:
        """
        Read data from a CSV file.
        
        Args:
            filename: Name of the CSV file (without extension)
            
        Returns:
            List of dictionaries representing CSV rows
        """
        filepath = os.path.join(self.data_dir, f"{filename}.csv")
        data = []
        
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Convert string values to appropriate types
                    processed_row = {}
                    for key, value in row.items():
                        if key in ['id', 'station1_id', 'station2_id', 'line_id', 'origin_id', 'destination_id']:
                            processed_row[key] = int(value) if value else None
                        elif key == 'price':
                            processed_row[key] = float(value) if value else 0.0
                        elif key == 'line_ids':
                            # Parse comma-separated line IDs
                            processed_row[key] = [int(x.strip()) for x in value.split(',')] if value else []
                        else:
                            processed_row[key] = value
                    data.append(processed_row)
        except FileNotFoundError:
            print(f"Warning: File {filepath} not found.")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
        
        return data
    
    def write_csv(self, filename: str, data: List[Dict[str, Any]], fieldnames: List[str] = None) -> bool:
        """
        Write data to a CSV file.
        
        Args:
            filename: Name of the CSV file (without extension)
            data: List of dictionaries to write
            fieldnames: List of column names (optional)
            
        Returns:
            True if successful, False otherwise
        """
        filepath = os.path.join(self.data_dir, f"{filename}.csv")
        
        try:
            # Ensure data directory exists
            os.makedirs(self.data_dir, exist_ok=True)
            
            if not data:
                return True
            
            # Get fieldnames from first row if not provided
            if fieldnames is None:
                fieldnames = list(data[0].keys())
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in data:
                    # Convert line_ids list back to comma-separated string
                    processed_row = {}
                    for key, value in row.items():
                        if key == 'line_ids' and isinstance(value, list):
                            processed_row[key] = ','.join(map(str, value))
                        else:
                            processed_row[key] = value
                    writer.writerow(processed_row)
            
            return True
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return False
    
    def append_to_csv(self, filename: str, data: Dict[str, Any], fieldnames: List[str] = None) -> bool:
        """
        Append a single row to a CSV file.
        
        Args:
            filename: Name of the CSV file (without extension)
            data: Dictionary representing the row to append
            fieldnames: List of column names (optional)
            
        Returns:
            True if successful, False otherwise
        """
        filepath = os.path.join(self.data_dir, f"{filename}.csv")
        
        try:
            # Check if file exists to determine if we need to write header
            file_exists = os.path.exists(filepath)
            
            # Get fieldnames from data if not provided
            if fieldnames is None:
                fieldnames = list(data.keys())
            
            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header only if file doesn't exist
                if not file_exists:
                    writer.writeheader()
                
                # Process line_ids if present
                processed_row = {}
                for key, value in data.items():
                    if key == 'line_ids' and isinstance(value, list):
                        processed_row[key] = ','.join(map(str, value))
                    else:
                        processed_row[key] = value
                
                writer.writerow(processed_row)
            
            return True
        except Exception as e:
            print(f"Error appending to {filepath}: {e}")
            return False
