# 🚇 Metro Ticket Purchasing System

A Python command-line application for purchasing metro tickets with Object-Oriented Programming principles, CSV data persistence, and interactive network visualization.

## ✨ Features

- 🚇 **Multi-line Metro Network**: Support for multiple metro lines with interchange stations
- 🎫 **Smart Ticket Purchasing**: Buy tickets with automatic shortest path calculation
- 💰 **Dynamic Pricing**: Price based on number of stations crossed ($2 base + $1 per station)
- 🗺️ **Interactive Visualization**: Beautiful network maps using matplotlib and networkx
- 📊 **Statistics & Analytics**: Track your ticket purchases and spending patterns
- 💾 **Data Persistence**: All data stored in CSV files for easy management
- 🔄 **Line Change Guidance**: Automatic step-by-step instructions for changing lines
- 🎯 **User-Friendly CLI**: Intuitive command-line interface

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd metro-system
   ```

2. **Install dependencies using Makefile (recommended)**
   ```bash
   make install
   ```
   
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   make run
   ```
   
   Or directly:
   ```bash
   python3 main.py
   ```

## 🎮 How to Use

### Main Menu Options

When you run the application, you'll see this menu:

```
==================================================
           METRO TICKET SYSTEM
==================================================
1. View all stations
2. Purchase ticket
3. View my tickets
4. Visualize metro network
5. View network information
6. View ticket statistics
7. Exit
==================================================
```

### Step-by-Step Usage

#### 1. **View All Stations**
- Choose option `1` to see all available metro stations
- Stations are organized by metro line
- Interchange stations are clearly marked

#### 2. **Purchase a Ticket**
- Choose option `2` to buy a ticket
- You'll see a list of all stations with their IDs
- Enter the origin station ID (e.g., `1`)
- Enter the destination station ID (e.g., `5`)
- The system will:
  - Calculate the shortest path
  - Determine the price
  - Generate step-by-step instructions
  - Save your ticket

#### 3. **View Your Tickets**
- Choose option `3` to see all your purchased tickets
- View ticket details including:
  - Ticket ID
  - Route and price
  - Purchase date
  - Travel path
- Optionally view detailed instructions for any ticket

#### 4. **Visualize Metro Network**
- Choose option `4` to see interactive network maps
- Options include:
  - Full network map
  - Specific line map
  - Interchange stations view
  - Save network image

#### 5. **View Network Information**
- Choose option `5` for network statistics
- See total stations, lines, and connections
- View interchange station details

#### 6. **View Ticket Statistics**
- Choose option `6` to see your usage analytics
- Track total spending and average prices
- Find your most-used routes

## 🗺️ Sample Metro Network

The system comes with a pre-configured metro network:

### Red Line (6 stations)
- Central Station (Interchange) ↔ North Square ↔ University ↔ City Center ↔ Market Place (Interchange) ↔ Station A

### Blue Line (5 stations)  
- Central Station (Interchange) ↔ Airport ↔ Stadium ↔ Library ↔ Theater ↔ Station B

### Green Line (4 stations)
- Market Place (Interchange) ↔ Park ↔ Mall ↔ Beach ↔ Station C

### Interchange Stations
- **Central Station**: Red Line ↔ Blue Line
- **Market Place**: Red Line ↔ Green Line

## 💰 Pricing System

- **Base Price**: $2.00 (for any ticket)
- **Per Station**: $1.00 additional for each station crossed
- **Examples**:
  - 1 station: $2.00 + $1.00 = $3.00
  - 3 stations: $2.00 + $3.00 = $5.00
  - 5 stations: $2.00 + $5.00 = $7.00

## 🏗️ Project Structure

```
metro-system/
├── main.py                    # 🚀 Entry point with CLI menu
├── models/                    # 🏛️ Core OOP classes
│   ├── station.py            # Station class
│   ├── metro_line.py         # MetroLine class  
│   ├── ticket.py             # Ticket class
│   ├── metro_network.py      # MetroNetwork class
│   └── ticket_manager.py     # TicketManager class
├── data/                     # 💾 CSV data files
│   ├── stations.csv          # Station data
│   ├── lines.csv             # Line data
│   ├── connections.csv       # Station connections
│   └── tickets.csv           # Purchased tickets
├── utils/                    # 🔧 Utility functions
│   ├── csv_handler.py        # CSV operations
│   └── path_finder.py        # Shortest path algorithm
├── visualization/            # 🎨 Network visualization
│   └── network_visualizer.py # Matplotlib graphs
├── requirements.txt          # 📦 Dependencies
├── Makefile                  # 🛠️ Build automation
└── README.md                 # 📖 This file
```

## 🛠️ Available Commands

Use the Makefile for easy project management:

```bash
make install    # Install all dependencies
make run        # Run the application
make test       # Run basic functionality tests
make clean      # Clean up temporary files
make help       # Show all available commands
```

## 🧪 Testing

Test the application functionality:

```bash
make test
```

This will verify:
- ✅ Network loading (15 stations, 3 lines)
- ✅ Pathfinding between stations
- ✅ Ticket purchasing
- ✅ Data persistence
- ✅ All modules import correctly

## 🔧 Technical Details

### Architecture
- **Language**: Python 3.7+
- **Paradigm**: Object-Oriented Programming
- **Data Storage**: CSV files
- **Pathfinding**: Breadth-First Search (BFS)
- **Visualization**: matplotlib + networkx

### Key Classes
- **Station**: Represents metro stations with interchange detection
- **MetroLine**: Manages metro lines and station ordering
- **Ticket**: Handles ticket data with UUID and pricing
- **MetroNetwork**: Core graph operations and pathfinding
- **TicketManager**: Ticket purchasing and management
- **NetworkVisualizer**: Interactive network maps

### Data Format
- **Stations**: ID, name, line IDs
- **Lines**: ID, name, color (for visualization)
- **Connections**: Station pairs with line information
- **Tickets**: Complete journey data with instructions

## 🎯 Example Usage Scenarios

### Scenario 1: Simple Journey
1. Start at Central Station (ID: 1)
2. Go to North Square (ID: 2)
3. **Result**: $3.00 ticket, 1 station crossed, Red Line

### Scenario 2: Line Change Journey
1. Start at Central Station (ID: 1)
2. Go to Park (ID: 10)
3. **Result**: $6.00 ticket, 4 stations crossed
4. **Instructions**: 
   - Take Red Line to Market Place
   - Change to Green Line
   - Continue to Park

### Scenario 3: Complex Journey
1. Start at Airport (ID: 6)
2. Go to Beach (ID: 12)
3. **Result**: $8.00 ticket, 6 stations crossed
4. **Instructions**:
   - Take Blue Line to Central Station
   - Change to Red Line
   - Go to Market Place
   - Change to Green Line
   - Continue to Beach

## 🐛 Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'matplotlib'"**
```bash
make install
# or
pip install matplotlib networkx
```

**"command not found: python"**
```bash
python3 main.py
# or
make run
```

**Import errors**
```bash
# Make sure you're in the project directory
cd metro-system
python3 main.py
```

### Getting Help

1. Check that all dependencies are installed: `make install`
2. Verify Python version: `python3 --version` (should be 3.7+)
3. Run tests: `make test`
4. Check the project structure matches the README


## 🤝 Contributing

Feel free to:
- Add new metro lines and stations
- Implement additional pricing models
- Enhance the visualization features
- Improve the CLI interface
- Add more comprehensive testing

---

**Happy Traveling! 🚇✨**

*Built with Python, Object-Oriented Programming, and lots of 🚇 enthusiasm!*
