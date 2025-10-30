"""
TicketManager for handling ticket operations.
"""
from typing import List, Optional, Dict, Any
from .ticket import Ticket
from .metro_network import MetroNetwork
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.csv_handler import CSVHandler


class TicketManager:
    """Manages ticket purchasing, storage, and retrieval."""
    
    def __init__(self, metro_network: MetroNetwork, data_dir: str = "data"):
        """
        Initialize the ticket manager.
        
        Args:
            metro_network: MetroNetwork instance for pathfinding and pricing
            data_dir: Directory containing CSV data files
        """
        self.metro_network = metro_network
        self.csv_handler = CSVHandler(data_dir)
        self.tickets = []  # List of Ticket objects
        self._load_tickets()
    
    def _load_tickets(self) -> None:
        """Load existing tickets from CSV file."""
        tickets_data = self.csv_handler.read_csv("tickets")
        for ticket_data in tickets_data:
            if ticket_data:  # Skip empty rows
                ticket = Ticket.from_dict(ticket_data)
                self.tickets.append(ticket)
    
    def purchase_ticket(self, origin_id: int, destination_id: int, 
                       base_price: float = 2.0, price_per_station: float = 1.0) -> Optional[Ticket]:
        """
        Purchase a ticket for travel between two stations.
        
        Args:
            origin_id: ID of the origin station
            destination_id: ID of the destination station
            base_price: Base price for any ticket
            price_per_station: Additional price per station crossed
            
        Returns:
            Ticket object if successful, None if failed
        """
        # Validate stations exist
        if origin_id not in self.metro_network.stations:
            print(f"Error: Origin station with ID {origin_id} not found.")
            return None
        
        if destination_id not in self.metro_network.stations:
            print(f"Error: Destination station with ID {destination_id} not found.")
            return None
        
        if origin_id == destination_id:
            print("Error: Origin and destination cannot be the same.")
            return None
        
        # Find shortest path
        path = self.metro_network.find_shortest_path(origin_id, destination_id)
        if not path:
            print("Error: No path found between the selected stations.")
            return None
        
        # Calculate price
        price = self.metro_network.calculate_ticket_price(path, base_price, price_per_station)
        
        # Generate instructions
        instructions = self.metro_network.get_travel_instructions(path)
        
        # Create ticket
        ticket = Ticket(
            origin_id=origin_id,
            destination_id=destination_id,
            price=price,
            path=path,
            instructions=instructions
        )
        
        # Add to tickets list
        self.tickets.append(ticket)
        
        # Save to CSV
        self._save_ticket_to_csv(ticket)
        
        return ticket
    
    def _save_ticket_to_csv(self, ticket: Ticket) -> bool:
        """
        Save a single ticket to CSV file.
        
        Args:
            ticket: Ticket object to save
            
        Returns:
            True if successful, False otherwise
        """
        return self.csv_handler.append_to_csv("tickets", ticket.to_dict())
    
    def view_tickets(self) -> None:
        """Display all purchased tickets."""
        if not self.tickets:
            print("\nNo tickets purchased yet.")
            return
        
        print(f"\n=== Your Tickets ({len(self.tickets)}) ===")
        for i, ticket in enumerate(self.tickets, 1):
            origin = self.metro_network.stations[ticket.origin_id]
            destination = self.metro_network.stations[ticket.destination_id]
            
            print(f"\n{i}. Ticket ID: {ticket.ticket_id[:8]}...")
            print(f"   Route: {origin.name} → {destination.name}")
            print(f"   Price: ${ticket.price:.2f}")
            print(f"   Purchase Date: {ticket.purchase_date}")
            print(f"   Path: {' → '.join([self.metro_network.stations[sid].name for sid in ticket.path])}")
    
    def view_ticket_details(self, ticket_id: str) -> None:
        """
        Display detailed information for a specific ticket.
        
        Args:
            ticket_id: ID of the ticket to view
        """
        ticket = self.get_ticket_by_id(ticket_id)
        if not ticket:
            print(f"Ticket with ID {ticket_id} not found.")
            return
        
        origin = self.metro_network.stations[ticket.origin_id]
        destination = self.metro_network.stations[ticket.destination_id]
        
        print(f"\n=== Ticket Details ===")
        print(f"Ticket ID: {ticket.ticket_id}")
        print(f"Route: {origin.name} → {destination.name}")
        print(f"Price: ${ticket.price:.2f}")
        print(f"Purchase Date: {ticket.purchase_date}")
        print(f"Stations Crossed: {len(ticket.path) - 1}")
        
        print(f"\n=== Travel Instructions ===")
        for i, instruction in enumerate(ticket.instructions, 1):
            print(f"{i}. {instruction}")
    
    def get_ticket_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Get a ticket by its ID.
        
        Args:
            ticket_id: ID of the ticket to find
            
        Returns:
            Ticket object or None if not found
        """
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None
    
    def get_tickets_by_route(self, origin_id: int, destination_id: int) -> List[Ticket]:
        """
        Get all tickets for a specific route.
        
        Args:
            origin_id: ID of the origin station
            destination_id: ID of the destination station
            
        Returns:
            List of Ticket objects for the route
        """
        return [ticket for ticket in self.tickets 
                if ticket.origin_id == origin_id and ticket.destination_id == destination_id]
    
    def get_total_spent(self) -> float:
        """
        Calculate total amount spent on tickets.
        
        Returns:
            Total amount spent
        """
        return sum(ticket.price for ticket in self.tickets)
    
    def get_ticket_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about purchased tickets.
        
        Returns:
            Dictionary with ticket statistics
        """
        if not self.tickets:
            return {
                'total_tickets': 0,
                'total_spent': 0.0,
                'average_price': 0.0,
                'most_used_route': None,
                'longest_journey': 0
            }
        
        # Count route usage
        route_counts = {}
        longest_journey = 0
        
        for ticket in self.tickets:
            route = f"{ticket.origin_id}-{ticket.destination_id}"
            route_counts[route] = route_counts.get(route, 0) + 1
            
            journey_length = len(ticket.path) - 1
            longest_journey = max(longest_journey, journey_length)
        
        # Find most used route
        most_used_route = max(route_counts.items(), key=lambda x: x[1])[0] if route_counts else None
        
        return {
            'total_tickets': len(self.tickets),
            'total_spent': self.get_total_spent(),
            'average_price': self.get_total_spent() / len(self.tickets),
            'most_used_route': most_used_route,
            'longest_journey': longest_journey
        }
    
    def display_statistics(self) -> None:
        """Display ticket purchase statistics."""
        stats = self.get_ticket_statistics()
        
        print(f"\n=== Ticket Statistics ===")
        print(f"Total Tickets: {stats['total_tickets']}")
        print(f"Total Spent: ${stats['total_spent']:.2f}")
        print(f"Average Price: ${stats['average_price']:.2f}")
        print(f"Longest Journey: {stats['longest_journey']} stations")
        
        if stats['most_used_route']:
            origin_id, dest_id = map(int, stats['most_used_route'].split('-'))
            origin = self.metro_network.stations[origin_id]
            destination = self.metro_network.stations[dest_id]
            print(f"Most Used Route: {origin.name} → {destination.name}")
    
    def save_all_tickets(self) -> bool:
        """
        Save all tickets to CSV file.
        
        Returns:
            True if successful, False otherwise
        """
        tickets_data = [ticket.to_dict() for ticket in self.tickets]
        return self.csv_handler.write_csv("tickets", tickets_data)
