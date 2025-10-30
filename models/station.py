"""
Station model for the metro system.
"""
from typing import List, Set


class Station:
    """Represents a metro station."""
    
    def __init__(self, station_id: int, name: str, line_ids: List[int] = None):
        """
        Initialize a station.
        
        Args:
            station_id: Unique identifier for the station
            name: Name of the station
            line_ids: List of line IDs that pass through this station
        """
        self.id = station_id
        self.name = name
        self.line_ids = line_ids or []
        self._lines = []  # Will be populated with MetroLine objects
    
    def add_line(self, metro_line) -> None:
        """Add a metro line to this station."""
        if metro_line not in self._lines:
            self._lines.append(metro_line)
    
    def is_interchange(self) -> bool:
        """Check if this station is an interchange (serves multiple lines)."""
        return len(self.line_ids) > 1
    
    def get_connected_stations(self, metro_network) -> List['Station']:
        """
        Get all stations directly connected to this station.
        
        Args:
            metro_network: MetroNetwork instance to get connections from
            
        Returns:
            List of connected Station objects
        """
        connected = []
        for station_id in metro_network.graph.get(self.id, []):
            connected.append(metro_network.stations[station_id])
        return connected
    
    def get_lines(self) -> List:
        """Get all MetroLine objects that pass through this station."""
        return self._lines
    
    def __str__(self) -> str:
        """String representation of the station."""
        interchange_indicator = " (Interchange)" if self.is_interchange() else ""
        return f"{self.name}{interchange_indicator}"
    
    def __repr__(self) -> str:
        """Detailed string representation of the station."""
        return f"Station(id={self.id}, name='{self.name}', lines={self.line_ids})"
