"""
Path finding algorithms for the metro system.
"""
from collections import deque
from typing import List, Dict, Set, Tuple, Optional


class PathFinder:
    """Handles pathfinding operations for the metro network."""
    
    @staticmethod
    def find_shortest_path(graph: Dict[int, List[int]], start: int, end: int) -> Optional[List[int]]:
        """
        Find the shortest path between two stations using BFS.
        
        Args:
            graph: Adjacency list representation of the metro network
            start: Starting station ID
            end: Destination station ID
            
        Returns:
            List of station IDs representing the shortest path, or None if no path exists
        """
        if start == end:
            return [start]
        
        if start not in graph or end not in graph:
            return None
        
        # BFS to find shortest path
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current_station, path = queue.popleft()
            
            # Check all connected stations
            for next_station in graph.get(current_station, []):
                if next_station == end:
                    return path + [next_station]
                
                if next_station not in visited:
                    visited.add(next_station)
                    queue.append((next_station, path + [next_station]))
        
        return None
    
    @staticmethod
    def find_all_paths(graph: Dict[int, List[int]], start: int, end: int, 
                      max_depth: int = 10) -> List[List[int]]:
        """
        Find all possible paths between two stations (up to max_depth).
        
        Args:
            graph: Adjacency list representation of the metro network
            start: Starting station ID
            end: Destination station ID
            max_depth: Maximum path length to consider
            
        Returns:
            List of all possible paths
        """
        if start == end:
            return [[start]]
        
        if start not in graph or end not in graph:
            return []
        
        all_paths = []
        queue = deque([(start, [start])])
        
        while queue:
            current_station, path = queue.popleft()
            
            # Stop if path is too long
            if len(path) > max_depth:
                continue
            
            # Check all connected stations
            for next_station in graph.get(current_station, []):
                if next_station == end:
                    all_paths.append(path + [next_station])
                elif next_station not in path:  # Avoid cycles
                    queue.append((next_station, path + [next_station]))
        
        return all_paths
    
    @staticmethod
    def calculate_path_distance(graph: Dict[int, List[int]], path: List[int]) -> int:
        """
        Calculate the distance (number of stations) for a given path.
        
        Args:
            graph: Adjacency list representation of the metro network
            path: List of station IDs representing the path
            
        Returns:
            Distance in number of stations crossed
        """
        if not path or len(path) < 2:
            return 0
        
        # Verify path is valid
        for i in range(len(path) - 1):
            current = path[i]
            next_station = path[i + 1]
            if next_station not in graph.get(current, []):
                return -1  # Invalid path
        
        return len(path) - 1  # Number of stations crossed (excluding origin)
    
    @staticmethod
    def get_station_connections(graph: Dict[int, List[int]], station_id: int) -> List[int]:
        """
        Get all stations directly connected to a given station.
        
        Args:
            graph: Adjacency list representation of the metro network
            station_id: ID of the station
            
        Returns:
            List of connected station IDs
        """
        return graph.get(station_id, [])
    
    @staticmethod
    def find_interchange_stations(stations: Dict[int, 'Station']) -> List[int]:
        """
        Find all interchange stations (stations serving multiple lines).
        
        Args:
            stations: Dictionary of station_id -> Station objects
            
        Returns:
            List of interchange station IDs
        """
        interchange_stations = []
        for station_id, station in stations.items():
            if station.is_interchange():
                interchange_stations.append(station_id)
        return interchange_stations
    
    @staticmethod
    def find_shortest_path_with_line_changes(graph: Dict[int, List[int]], 
                                           stations: Dict[int, 'Station'],
                                           start: int, end: int) -> Tuple[Optional[List[int]], int]:
        """
        Find shortest path and count line changes.
        
        Args:
            graph: Adjacency list representation of the metro network
            stations: Dictionary of station_id -> Station objects
            start: Starting station ID
            end: Destination station ID
            
        Returns:
            Tuple of (path, number_of_line_changes)
        """
        path = PathFinder.find_shortest_path(graph, start, end)
        if not path:
            return None, 0
        
        line_changes = 0
        current_lines = set()
        
        for i, station_id in enumerate(path):
            station = stations.get(station_id)
            if not station:
                continue
            
            station_lines = set(station.line_ids)
            
            if i == 0:
                # Starting station
                current_lines = station_lines
            else:
                # Check if we need to change lines
                if not current_lines.intersection(station_lines):
                    # No common lines, need to change
                    line_changes += 1
                    current_lines = station_lines
                else:
                    # Update current lines to intersection
                    current_lines = current_lines.intersection(station_lines)
        
        return path, line_changes
