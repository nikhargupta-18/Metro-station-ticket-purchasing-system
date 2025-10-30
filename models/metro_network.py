"""
MetroNetwork model for managing the entire metro system.
"""
from typing import Dict, List, Optional, Tuple
from .station import Station
from .metro_line import MetroLine
from .ticket import Ticket
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.csv_handler import CSVHandler
from utils.path_finder import PathFinder


class MetroNetwork:
    """Manages the entire metro network including stations, lines, and routing."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the metro network.
        
        Args:
            data_dir: Directory containing CSV data files
        """
        self.data_dir = data_dir
        self.csv_handler = CSVHandler(data_dir)
        self.stations = {}  # station_id -> Station
        self.lines = {}     # line_id -> MetroLine
        self.graph = {}     # station_id -> [connected_station_ids]
        self._load_data()
    
    def _load_data(self) -> None:
        """Load all data from CSV files."""
        self._load_lines()
        self._load_stations()
        self._load_connections()
    
    def _load_lines(self) -> None:
        """Load metro lines from CSV."""
        lines_data = self.csv_handler.read_csv("lines")
        for line_data in lines_data:
            line = MetroLine(
                line_id=line_data['id'],
                name=line_data['name'],
                color=line_data['color']
            )
            self.lines[line.id] = line
    
    def _load_stations(self) -> None:
        """Load stations from CSV."""
        stations_data = self.csv_handler.read_csv("stations")
        for station_data in stations_data:
            station = Station(
                station_id=station_data['id'],
                name=station_data['name'],
                line_ids=station_data['line_ids']
            )
            self.stations[station.id] = station
            
            # Add station to its lines
            for line_id in station.line_ids:
                if line_id in self.lines:
                    self.lines[line_id].add_station(station)
    
    def _load_connections(self) -> None:
        """Load station connections from CSV and build graph."""
        connections_data = self.csv_handler.read_csv("connections")
        
        # Initialize graph
        for station_id in self.stations:
            self.graph[station_id] = []
        
        # Add connections
        for conn_data in connections_data:
            station1_id = conn_data['station1_id']
            station2_id = conn_data['station2_id']
            
            if station1_id in self.stations and station2_id in self.stations:
                # Add bidirectional connection
                if station2_id not in self.graph[station1_id]:
                    self.graph[station1_id].append(station2_id)
                if station1_id not in self.graph[station2_id]:
                    self.graph[station2_id].append(station1_id)
    
    def find_shortest_path(self, start_id: int, end_id: int) -> Optional[List[int]]:
        """
        Find the shortest path between two stations.
        
        Args:
            start_id: Starting station ID
            end_id: Destination station ID
            
        Returns:
            List of station IDs representing the shortest path, or None if no path exists
        """
        return PathFinder.find_shortest_path(self.graph, start_id, end_id)
    
    def calculate_ticket_price(self, path: List[int], base_price: float = 2.0, 
                             price_per_station: float = 1.0) -> float:
        """
        Calculate ticket price based on the path.
        
        Args:
            path: List of station IDs in the journey
            base_price: Base price for any ticket
            price_per_station: Additional price per station crossed
            
        Returns:
            Calculated price
        """
        if not path or len(path) < 2:
            return base_price
        
        stations_crossed = len(path) - 1
        return base_price + (stations_crossed * price_per_station)
    
    def get_travel_instructions(self, path: List[int]) -> List[str]:
        """
        Generate travel instructions for a given path.
        
        Args:
            path: List of station IDs in the journey
            
        Returns:
            List of instruction strings
        """
        if not path or len(path) < 2:
            return ["Invalid path"]
        
        instructions = []
        current_line = None
        
        for i, station_id in enumerate(path):
            station = self.stations.get(station_id)
            if not station:
                continue
            
            if i == 0:
                # Origin station
                instructions.append(f"Start at {station.name}")
                if station.is_interchange():
                    line_names = [self.lines[line_id].name for line_id in station.line_ids]
                    instructions.append(f"  - This is an interchange station serving lines: {', '.join(line_names)}")
            elif i == len(path) - 1:
                # Destination station
                instructions.append(f"Arrive at {station.name}")
            else:
                # Intermediate stations
                next_station = self.stations.get(path[i + 1])
                if next_station:
                    # Find common line between current and next station
                    common_lines = set(station.line_ids) & set(next_station.line_ids)
                    
                    if current_line and current_line.id not in common_lines:
                        # Need to change lines
                        if common_lines:
                            new_line = self.lines[list(common_lines)[0]]
                            instructions.append(f"Change from {self.lines[current_line.id].name} to {new_line.name} Line")
                            current_line = new_line
                    elif not current_line and common_lines:
                        # First line assignment
                        current_line = self.lines[list(common_lines)[0]]
                        instructions.append(f"Take {current_line.name} Line")
                    
                    instructions.append(f"Pass through {station.name}")
        
        return instructions
    
    def get_station_by_name(self, name: str) -> Optional[Station]:
        """
        Find a station by its name (case-insensitive).
        
        Args:
            name: Name of the station to find
            
        Returns:
            Station object or None if not found
        """
        name_lower = name.lower()
        for station in self.stations.values():
            if station.name.lower() == name_lower:
                return station
        return None
    
    def get_stations_by_line(self, line_id: int) -> List[Station]:
        """
        Get all stations on a specific line.
        
        Args:
            line_id: ID of the line
            
        Returns:
            List of Station objects on the line
        """
        if line_id not in self.lines:
            return []
        return self.lines[line_id].stations
    
    def get_interchange_stations(self) -> List[Station]:
        """
        Get all interchange stations.
        
        Returns:
            List of interchange Station objects
        """
        return [station for station in self.stations.values() if station.is_interchange()]
    
    def get_network_stats(self) -> Dict[str, int]:
        """
        Get basic statistics about the network.
        
        Returns:
            Dictionary with network statistics
        """
        return {
            'total_stations': len(self.stations),
            'total_lines': len(self.lines),
            'interchange_stations': len(self.get_interchange_stations()),
            'total_connections': sum(len(connections) for connections in self.graph.values()) // 2
        }
    
    def display_stations(self) -> None:
        """Display all stations in the network."""
        print("\n=== Metro Stations ===")
        for line_id, line in self.lines.items():
            print(f"\n{line.name} ({line.color}):")
            for station in line.stations:
                interchange_indicator = " (Interchange)" if station.is_interchange() else ""
                print(f"  - {station.name}{interchange_indicator}")
    
    def display_network_info(self) -> None:
        """Display comprehensive network information."""
        stats = self.get_network_stats()
        print("\n=== Metro Network Information ===")
        print(f"Total Stations: {stats['total_stations']}")
        print(f"Total Lines: {stats['total_lines']}")
        print(f"Interchange Stations: {stats['interchange_stations']}")
        print(f"Total Connections: {stats['total_connections']}")
        
        print("\n=== Interchange Stations ===")
        for station in self.get_interchange_stations():
            line_names = [self.lines[line_id].name for line_id in station.line_ids]
            print(f"- {station.name}: {', '.join(line_names)}")
    
    def validate_path(self, path: List[int]) -> bool:
        """
        Validate if a path is valid in the network.
        
        Args:
            path: List of station IDs to validate
            
        Returns:
            True if path is valid, False otherwise
        """
        if not path or len(path) < 2:
            return False
        
        for i in range(len(path) - 1):
            current = path[i]
            next_station = path[i + 1]
            
            if current not in self.stations or next_station not in self.stations:
                return False
            
            if next_station not in self.graph.get(current, []):
                return False
        
        return True
