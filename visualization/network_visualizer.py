"""
Network visualization for the metro system using matplotlib and networkx.
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Dict, List, Optional, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.metro_network import MetroNetwork
from models.station import Station
from models.metro_line import MetroLine


class NetworkVisualizer:
    """Handles visualization of the metro network."""
    
    def __init__(self, metro_network: MetroNetwork):
        """
        Initialize the network visualizer.
        
        Args:
            metro_network: MetroNetwork instance to visualize
        """
        self.metro_network = metro_network
        self.graph = nx.Graph()
        self._build_networkx_graph()
    
    def _build_networkx_graph(self) -> None:
        """Build NetworkX graph from metro network data."""
        # Add all stations as nodes
        for station_id, station in self.metro_network.stations.items():
            self.graph.add_node(
                station_id,
                name=station.name,
                is_interchange=station.is_interchange(),
                line_ids=station.line_ids
            )
        
        # Add all connections as edges
        for station_id, connections in self.metro_network.graph.items():
            for connected_id in connections:
                if station_id < connected_id:  # Avoid duplicate edges
                    # Find common line for edge color
                    station = self.metro_network.stations[station_id]
                    connected = self.metro_network.stations[connected_id]
                    common_lines = set(station.line_ids) & set(connected.line_ids)
                    
                    line_id = list(common_lines)[0] if common_lines else None
                    self.graph.add_edge(
                        station_id, 
                        connected_id,
                        line_id=line_id
                    )
    
    def visualize_network(self, figsize: Tuple[int, int] = (15, 10), 
                         show_labels: bool = True, 
                         highlight_path: Optional[List[int]] = None) -> None:
        """
        Visualize the metro network.
        
        Args:
            figsize: Figure size (width, height)
            show_labels: Whether to show station names
            highlight_path: Optional path to highlight in different color
        """
        plt.figure(figsize=figsize)
        
        # Use spring layout for better positioning
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Draw edges for each line separately
        for line_id, line in self.metro_network.lines.items():
            # Get edges for this line
            line_edges = [(u, v) for u, v, d in self.graph.edges(data=True) 
                         if d.get('line_id') == line_id]
            
            if line_edges:
                nx.draw_networkx_edges(
                    self.graph, pos,
                    edgelist=line_edges,
                    edge_color=line.color,
                    width=3,
                    alpha=0.7,
                    label=line.name
                )
        
        # Highlight specific path if provided
        if highlight_path and len(highlight_path) > 1:
            path_edges = [(highlight_path[i], highlight_path[i + 1]) 
                         for i in range(len(highlight_path) - 1)]
            nx.draw_networkx_edges(
                self.graph, pos,
                edgelist=path_edges,
                edge_color='red',
                width=5,
                alpha=0.9
            )
        
        # Draw nodes
        # Separate interchange and regular stations
        interchange_nodes = [node for node, data in self.graph.nodes(data=True) 
                           if data.get('is_interchange', False)]
        regular_nodes = [node for node, data in self.graph.nodes(data=True) 
                        if not data.get('is_interchange', False)]
        
        # Draw regular stations
        if regular_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=regular_nodes,
                node_color='lightblue',
                node_size=300,
                alpha=0.8
            )
        
        # Draw interchange stations
        if interchange_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=interchange_nodes,
                node_color='orange',
                node_size=500,
                alpha=0.9
            )
        
        # Draw labels
        if show_labels:
            labels = {node: data['name'] for node, data in self.graph.nodes(data=True)}
            nx.draw_networkx_labels(
                self.graph, pos,
                labels=labels,
                font_size=8,
                font_weight='bold'
            )
        
        # Add legend
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Set title and layout
        plt.title("Metro Network Map", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Show the plot
        plt.show()
    
    def visualize_line(self, line_id: int, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Visualize a specific metro line.
        
        Args:
            line_id: ID of the line to visualize
            figsize: Figure size (width, height)
        """
        if line_id not in self.metro_network.lines:
            print(f"Line with ID {line_id} not found.")
            return
        
        line = self.metro_network.lines[line_id]
        
        plt.figure(figsize=figsize)
        
        # Create subgraph for this line
        line_nodes = [station.id for station in line.stations]
        line_subgraph = self.graph.subgraph(line_nodes)
        
        # Use linear layout for line visualization
        pos = {}
        for i, station_id in enumerate(line_nodes):
            pos[station_id] = (i, 0)
        
        # Draw the line
        nx.draw_networkx_edges(
            line_subgraph, pos,
            edge_color=line.color,
            width=5,
            alpha=0.8
        )
        
        # Draw stations
        nx.draw_networkx_nodes(
            line_subgraph, pos,
            node_color=line.color,
            node_size=400,
            alpha=0.8
        )
        
        # Draw labels
        labels = {node: self.metro_network.stations[node].name 
                 for node in line_nodes}
        nx.draw_networkx_labels(
            line_subgraph, pos,
            labels=labels,
            font_size=10,
            font_weight='bold'
        )
        
        plt.title(f"{line.name} - Station Map", fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def visualize_interchanges(self, figsize: Tuple[int, int] = (10, 8)) -> None:
        """
        Visualize interchange stations and their connections.
        
        Args:
            figsize: Figure size (width, height)
        """
        interchange_stations = self.metro_network.get_interchange_stations()
        
        if not interchange_stations:
            print("No interchange stations found.")
            return
        
        plt.figure(figsize=figsize)
        
        # Create subgraph with interchange stations and their neighbors
        interchange_nodes = [station.id for station in interchange_stations]
        neighbor_nodes = set()
        
        for station in interchange_stations:
            for neighbor_id in self.metro_network.graph.get(station.id, []):
                neighbor_nodes.add(neighbor_id)
        
        all_nodes = set(interchange_nodes) | neighbor_nodes
        subgraph = self.graph.subgraph(all_nodes)
        
        # Use circular layout
        pos = nx.circular_layout(subgraph)
        
        # Draw edges
        nx.draw_networkx_edges(
            subgraph, pos,
            edge_color='gray',
            width=2,
            alpha=0.6
        )
        
        # Draw neighbor stations
        neighbor_only = [node for node in all_nodes if node not in interchange_nodes]
        if neighbor_only:
            nx.draw_networkx_nodes(
                subgraph, pos,
                nodelist=neighbor_only,
                node_color='lightblue',
                node_size=200,
                alpha=0.7
            )
        
        # Draw interchange stations
        nx.draw_networkx_nodes(
            subgraph, pos,
            nodelist=interchange_nodes,
            node_color='red',
            node_size=400,
            alpha=0.9
        )
        
        # Draw labels
        labels = {node: self.metro_network.stations[node].name 
                 for node in all_nodes}
        nx.draw_networkx_labels(
            subgraph, pos,
            labels=labels,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title("Interchange Stations and Connections", fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    
    def save_network_image(self, filename: str, figsize: Tuple[int, int] = (15, 10)) -> None:
        """
        Save network visualization to file.
        
        Args:
            filename: Name of the file to save (without extension)
            figsize: Figure size (width, height)
        """
        plt.figure(figsize=figsize)
        
        # Use spring layout
        pos = nx.spring_layout(self.graph, k=3, iterations=50)
        
        # Draw edges for each line
        for line_id, line in self.metro_network.lines.items():
            line_edges = [(u, v) for u, v, d in self.graph.edges(data=True) 
                         if d.get('line_id') == line_id]
            
            if line_edges:
                nx.draw_networkx_edges(
                    self.graph, pos,
                    edgelist=line_edges,
                    edge_color=line.color,
                    width=3,
                    alpha=0.7
                )
        
        # Draw nodes
        interchange_nodes = [node for node, data in self.graph.nodes(data=True) 
                           if data.get('is_interchange', False)]
        regular_nodes = [node for node, data in self.graph.nodes(data=True) 
                        if not data.get('is_interchange', False)]
        
        if regular_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=regular_nodes,
                node_color='lightblue',
                node_size=300,
                alpha=0.8
            )
        
        if interchange_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=interchange_nodes,
                node_color='orange',
                node_size=500,
                alpha=0.9
            )
        
        # Draw labels
        labels = {node: data['name'] for node, data in self.graph.nodes(data=True)}
        nx.draw_networkx_labels(
            self.graph, pos,
            labels=labels,
            font_size=8,
            font_weight='bold'
        )
        
        plt.title("Metro Network Map", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(f"{filename}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Network map saved as {filename}.png")
