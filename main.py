#!/usr/bin/env python3
"""
Metro Ticket Purchasing System - Main Application
Command-line interface for purchasing metro tickets.
"""
import sys
import os
from typing import Optional

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.metro_network import MetroNetwork
from models.ticket_manager import TicketManager
from visualization.network_visualizer import NetworkVisualizer


class MetroTicketSystem:
    """Main application class for the Metro Ticket System."""
    
    def __init__(self):
        """Initialize the metro ticket system."""
        print("🚇 Welcome to the Metro Ticket Purchasing System! 🚇")
        print("Loading metro network...")
        
        try:
            self.metro_network = MetroNetwork()
            self.ticket_manager = TicketManager(self.metro_network)
            self.visualizer = NetworkVisualizer(self.metro_network)
            print("✅ Metro network loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading metro network: {e}")
            sys.exit(1)
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("           METRO TICKET SYSTEM")
        print("="*50)
        print("1. View all stations")
        print("2. Purchase ticket")
        print("3. View my tickets")
        print("4. Visualize metro network")
        print("5. View network information")
        print("6. View ticket statistics")
        print("7. Exit")
        print("="*50)
    
    def view_stations(self) -> None:
        """Display all metro stations."""
        self.metro_network.display_stations()
        input("\nPress Enter to continue...")
    
    def purchase_ticket(self) -> None:
        """Handle ticket purchasing."""
        print("\n=== Purchase Ticket ===")
        
        # Display stations for reference
        print("\nAvailable stations:")
        for station_id, station in self.metro_network.stations.items():
            print(f"{station_id:2d}. {station.name}")
        
        try:
            # Get origin station
            origin_id = int(input("\nEnter origin station ID: "))
            if origin_id not in self.metro_network.stations:
                print("❌ Invalid origin station ID.")
                return
            
            # Get destination station
            dest_id = int(input("Enter destination station ID: "))
            if dest_id not in self.metro_network.stations:
                print("❌ Invalid destination station ID.")
                return
            
            if origin_id == dest_id:
                print("❌ Origin and destination cannot be the same.")
                return
            
            # Purchase ticket
            print("\nProcessing your ticket...")
            ticket = self.ticket_manager.purchase_ticket(origin_id, dest_id)
            
            if ticket:
                origin = self.metro_network.stations[origin_id]
                destination = self.metro_network.stations[dest_id]
                
                print(f"\n✅ Ticket purchased successfully!")
                print(f"Ticket ID: {ticket.ticket_id}")
                print(f"Route: {origin.name} → {destination.name}")
                print(f"Price: ${ticket.price:.2f}")
                print(f"Stations to cross: {len(ticket.path) - 1}")
                
                # Show travel instructions
                print(f"\n=== Travel Instructions ===")
                for i, instruction in enumerate(ticket.instructions, 1):
                    print(f"{i}. {instruction}")
            else:
                print("❌ Failed to purchase ticket.")
        
        except ValueError:
            print("❌ Please enter valid station IDs (numbers only).")
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled.")
        
        input("\nPress Enter to continue...")
    
    def view_tickets(self) -> None:
        """Display purchased tickets."""
        self.ticket_manager.view_tickets()
        
        # Option to view detailed ticket
        if self.ticket_manager.tickets:
            try:
                ticket_id = input("\nEnter ticket ID to view details (or press Enter to skip): ").strip()
                if ticket_id:
                    self.ticket_manager.view_ticket_details(ticket_id)
            except KeyboardInterrupt:
                pass
        
        input("\nPress Enter to continue...")
    
    def visualize_network(self) -> None:
        """Display network visualization."""
        print("\n=== Metro Network Visualization ===")
        print("Choose visualization type:")
        print("1. Full network map")
        print("2. Specific line map")
        print("3. Interchange stations")
        print("4. Save network image")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("Generating full network map...")
                self.visualizer.visualize_network()
            
            elif choice == "2":
                print("\nAvailable lines:")
                for line_id, line in self.metro_network.lines.items():
                    print(f"{line_id}. {line.name}")
                
                line_id = int(input("Enter line ID: "))
                if line_id in self.metro_network.lines:
                    print(f"Generating {self.metro_network.lines[line_id].name} map...")
                    self.visualizer.visualize_line(line_id)
                else:
                    print("❌ Invalid line ID.")
            
            elif choice == "3":
                print("Generating interchange stations map...")
                self.visualizer.visualize_interchanges()
            
            elif choice == "4":
                filename = input("Enter filename (without extension): ").strip()
                if filename:
                    print("Saving network image...")
                    self.visualizer.save_network_image(filename)
                else:
                    print("❌ Invalid filename.")
            
            else:
                print("❌ Invalid choice.")
        
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n❌ Operation cancelled.")
        except Exception as e:
            print(f"❌ Error generating visualization: {e}")
            print("Make sure matplotlib and networkx are installed:")
            print("pip install matplotlib networkx")
        
        input("\nPress Enter to continue...")
    
    def view_network_info(self) -> None:
        """Display network information."""
        self.metro_network.display_network_info()
        input("\nPress Enter to continue...")
    
    def view_statistics(self) -> None:
        """Display ticket statistics."""
        self.ticket_manager.display_statistics()
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Run the main application loop."""
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == "1":
                    self.view_stations()
                elif choice == "2":
                    self.purchase_ticket()
                elif choice == "3":
                    self.view_tickets()
                elif choice == "4":
                    self.visualize_network()
                elif choice == "5":
                    self.view_network_info()
                elif choice == "6":
                    self.view_statistics()
                elif choice == "7":
                    print("\n👋 Thank you for using the Metro Ticket System!")
                    print("Have a great journey! 🚇")
                    break
                else:
                    print("❌ Invalid choice. Please enter a number between 1-7.")
                    input("Press Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Main entry point."""
    try:
        app = MetroTicketSystem()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
