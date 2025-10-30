"""
MetroLine model for the metro system.
"""
from typing import List, Optional


class MetroLine:
    """Represents a metro line."""
    
    def __init__(self, line_id: int, name: str, color: str = "#000000"):
        """
        Initialize a metro line.
        
        Args:
            line_id: Unique identifier for the line
            name: Name of the line
            color: Color code for visualization (hex format)
        """
        self.id = line_id
        self.name = name
        self.color = color
        self.stations = []  # Ordered list of Station objects
    
    def add_station(self, station, position: Optional[int] = None) -> None:
        """
        Add a station to this line.
        
        Args:
            station: Station object to add
            position: Position to insert at (None for end)
        """
        if position is None:
            self.stations.append(station)
        else:
            self.stations.insert(position, station)
        
        # Add this line to the station
        station.add_line(self)
    
    def get_station_index(self, station_id: int) -> Optional[int]:
        """
        Get the index of a station in this line.
        
        Args:
            station_id: ID of the station to find
            
        Returns:
            Index of the station, or None if not found
        """
        for i, station in enumerate(self.stations):
            if station.id == station_id:
                return i
        return None
    
    def get_station_by_index(self, index: int) -> Optional['Station']:
        """
        Get station at a specific index.
        
        Args:
            index: Index of the station
            
        Returns:
            Station object or None if index is out of range
        """
        if 0 <= index < len(self.stations):
            return self.stations[index]
        return None
    
    def get_adjacent_stations(self, station_id: int) -> List['Station']:
        """
        Get stations adjacent to the given station on this line.
        
        Args:
            station_id: ID of the station
            
        Returns:
            List of adjacent Station objects
        """
        index = self.get_station_index(station_id)
        if index is None:
            return []
        
        adjacent = []
        if index > 0:
            adjacent.append(self.stations[index - 1])
        if index < len(self.stations) - 1:
            adjacent.append(self.stations[index + 1])
        
        return adjacent
    
    def __str__(self) -> str:
        """String representation of the line."""
        return f"{self.name} Line"
    
    def __repr__(self) -> str:
        """Detailed string representation of the line."""
        return f"MetroLine(id={self.id}, name='{self.name}', color='{self.color}', stations={len(self.stations)})"
