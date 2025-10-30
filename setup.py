#!/usr/bin/env python3
"""
Metro Ticket System - Setup Script
Automated setup and installation script for the Metro Ticket Purchasing System.
"""
import sys
import os
import subprocess
import platform

def print_header():
    """Print setup header."""
    print("🚇 Metro Ticket Purchasing System - Setup")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_data_files():
    """Check if data files exist."""
    print("\n📊 Checking data files...")
    data_files = ["data/stations.csv", "data/lines.csv", "data/connections.csv", "data/tickets.csv"]
    missing_files = []
    
    for file in data_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing data files: {', '.join(missing_files)}")
        return False
    
    print("✅ All data files present")
    return True

def test_imports():
    """Test if all modules can be imported."""
    print("\n🧪 Testing module imports...")
    try:
        from models.metro_network import MetroNetwork
        from models.ticket_manager import TicketManager
        from visualization.network_visualizer import NetworkVisualizer
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_basic_test():
    """Run basic functionality test."""
    print("\n🔬 Running basic functionality test...")
    try:
        from models.metro_network import MetroNetwork
        from models.ticket_manager import TicketManager
        
        # Test network loading
        metro = MetroNetwork()
        print(f"✅ Network loaded: {len(metro.stations)} stations, {len(metro.lines)} lines")
        
        # Test ticket manager
        ticket_mgr = TicketManager(metro)
        print(f"✅ Ticket manager initialized: {len(ticket_mgr.tickets)} existing tickets")
        
        # Test pathfinding
        station_ids = list(metro.stations.keys())
        if len(station_ids) >= 2:
            path = metro.find_shortest_path(station_ids[0], station_ids[-1])
            print(f"✅ Pathfinding test: {len(path)} stations in path")
        
        print("✅ All tests passed")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        print("❌ Data files are missing. Please ensure all CSV files are present.")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Module import failed. Check dependencies installation.")
        sys.exit(1)
    
    # Run basic test
    if not run_basic_test():
        print("❌ Basic functionality test failed.")
        sys.exit(1)
    
    # Success
    print("\n🎉 Setup completed successfully!")
    print("\n💡 Next steps:")
    print("   python3 main.py          # Run the application")
    print("   make run                 # Or use Makefile")
    print("   make help                # See all available commands")
    print("\n🚇 Happy traveling!")

if __name__ == "__main__":
    main()
