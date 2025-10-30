"""
Ticket model for the metro system.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any


class Ticket:
    """Represents a metro ticket."""
    
    def __init__(self, origin_id: int, destination_id: int, price: float = 0.0, 
                 path: List[int] = None, instructions: List[str] = None):
        """
        Initialize a ticket.
        
        Args:
            origin_id: ID of the origin station
            destination_id: ID of the destination station
            price: Price of the ticket
            path: List of station IDs in the journey path
            instructions: List of step-by-step instructions
        """
        self.ticket_id = str(uuid.uuid4())
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.price = price
        self.path = path or []
        self.instructions = instructions or []
        self.purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate_price(self, base_price: float = 2.0, price_per_station: float = 1.0) -> float:
        """
        Calculate ticket price based on the number of stations.
        
        Args:
            base_price: Base price for any ticket
            price_per_station: Additional price per station crossed
            
        Returns:
            Calculated price
        """
        if not self.path:
            return base_price
        
        # Number of stations crossed (excluding origin)
        stations_crossed = len(self.path) - 1
        return base_price + (stations_crossed * price_per_station)
    
    def generate_instructions(self, metro_network) -> List[str]:
        """
        Generate step-by-step travel instructions.
        
        Args:
            metro_network: MetroNetwork instance to get station and line information
            
        Returns:
            List of instruction strings
        """
        if not self.path or len(self.path) < 2:
            return ["Invalid path"]
        
        instructions = []
        current_line = None
        
        for i, station_id in enumerate(self.path):
            station = metro_network.stations.get(station_id)
            if not station:
                continue
            
            if i == 0:
                # Origin station
                instructions.append(f"Start at {station.name}")
                if station.is_interchange():
                    instructions.append(f"  - This is an interchange station serving lines: {', '.join([metro_network.lines[line_id].name for line_id in station.line_ids])}")
            elif i == len(self.path) - 1:
                # Destination station
                instructions.append(f"Arrive at {station.name}")
            else:
                # Intermediate stations
                # Check if we need to change lines
                next_station = metro_network.stations.get(self.path[i + 1])
                if next_station:
                    # Find common line between current and next station
                    common_lines = set(station.line_ids) & set(next_station.line_ids)
                    
                    if current_line and current_line.id not in common_lines:
                        # Need to change lines
                        new_line = metro_network.lines[list(common_lines)[0]]
                        instructions.append(f"Change from {metro_network.lines[current_line.id].name} to {new_line.name} Line")
                        current_line = new_line
                    elif not current_line and common_lines:
                        # First line assignment
                        current_line = metro_network.lines[list(common_lines)[0]]
                        instructions.append(f"Take {current_line.name} Line")
                    
                    instructions.append(f"Pass through {station.name}")
        
        return instructions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ticket to dictionary for CSV storage."""
        return {
            'ticket_id': self.ticket_id,
            'origin_id': self.origin_id,
            'destination_id': self.destination_id,
            'price': self.price,
            'path': ','.join(map(str, self.path)),
            'instructions': '|'.join(self.instructions),
            'purchase_date': self.purchase_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ticket':
        """Create ticket from dictionary (for loading from CSV)."""
        ticket = cls(
            origin_id=data['origin_id'],
            destination_id=data['destination_id'],
            price=data['price'],
            path=[int(x) for x in data['path'].split(',')] if data['path'] else [],
            instructions=data['instructions'].split('|') if data['instructions'] else []
        )
        ticket.ticket_id = data['ticket_id']
        ticket.purchase_date = data['purchase_date']
        return ticket
    
    def __str__(self) -> str:
        """String representation of the ticket."""
        return f"Ticket {self.ticket_id[:8]}... ({self.origin_id} → {self.destination_id}) - ${self.price:.2f}"
    
    def __repr__(self) -> str:
        """Detailed string representation of the ticket."""
        return f"Ticket(id={self.ticket_id}, origin={self.origin_id}, dest={self.destination_id}, price={self.price})"
