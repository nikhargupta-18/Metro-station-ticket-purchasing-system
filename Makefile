# Metro Ticket Purchasing System - Makefile
# Author: Metro System Team
# Description: Build automation for the Metro Ticket System

# Variables
PYTHON := python3
PIP := pip3
PROJECT_NAME := metro-system
MAIN_FILE := main.py
REQUIREMENTS := requirements.txt
DATA_DIR := data

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
WHITE := \033[1;37m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Show this help message
	@echo "$(CYAN)🚇 Metro Ticket Purchasing System - Available Commands$(NC)"
	@echo "$(WHITE)================================================$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)💡 Quick Start:$(NC)"
	@echo "  make install  # Install dependencies"
	@echo "  make run      # Run the application"
	@echo "  make test     # Test functionality"
	@echo ""

# Installation targets
.PHONY: install
install: check-python install-deps ## Install all dependencies
	@echo "$(GREEN)✅ Installation complete!$(NC)"
	@echo "$(YELLOW)💡 Run 'make run' to start the application$(NC)"

.PHONY: check-python
check-python: ## Check Python version
	@echo "$(BLUE)🔍 Checking Python version...$(NC)"
	@$(PYTHON) --version || (echo "$(RED)❌ Python3 not found. Please install Python 3.7+$(NC)" && exit 1)
	@echo "$(GREEN)✅ Python version check passed$(NC)"

.PHONY: install-deps
install-deps: ## Install Python dependencies
	@echo "$(BLUE)📦 Installing Python dependencies...$(NC)"
	@$(PIP) install -r $(REQUIREMENTS) || (echo "$(RED)❌ Failed to install dependencies$(NC)" && exit 1)
	@echo "$(GREEN)✅ Dependencies installed successfully$(NC)"

# Application targets
.PHONY: run
run: check-deps ## Run the Metro Ticket System
	@echo "$(PURPLE)🚇 Starting Metro Ticket System...$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to exit$(NC)"
	@echo ""
	@$(PYTHON) $(MAIN_FILE)

.PHONY: run-quiet
run-quiet: check-deps ## Run the application quietly (for testing)
	@$(PYTHON) $(MAIN_FILE) > /dev/null 2>&1 &

# Testing targets
.PHONY: test
test: check-deps ## Run basic functionality tests
	@echo "$(BLUE)🧪 Running Metro System tests...$(NC)"
	@$(PYTHON) -c "\
	from models.metro_network import MetroNetwork; \
	from models.ticket_manager import TicketManager; \
	print('✅ Network loading test passed'); \
	metro = MetroNetwork(); \
	print(f'✅ Loaded {len(metro.stations)} stations and {len(metro.lines)} lines'); \
	ticket_mgr = TicketManager(metro); \
	print('✅ Ticket manager initialized'); \
	station_ids = list(metro.stations.keys()); \
	path = metro.find_shortest_path(station_ids[0], station_ids[-1]); \
	print(f'✅ Pathfinding test passed: {len(path)} stations'); \
	ticket = ticket_mgr.purchase_ticket(station_ids[0], station_ids[1]); \
	print(f'✅ Ticket purchase test passed: ${ticket.price:.2f}'); \
	print('🎉 All tests passed successfully!'); \
	"
	@echo "$(GREEN)✅ All tests completed successfully!$(NC)"

.PHONY: test-imports
test-imports: ## Test all module imports
	@echo "$(BLUE)🔍 Testing module imports...$(NC)"
	@$(PYTHON) -c "from models.metro_network import MetroNetwork; print('✅ MetroNetwork import OK')"
	@$(PYTHON) -c "from models.ticket_manager import TicketManager; print('✅ TicketManager import OK')"
	@$(PYTHON) -c "from visualization.network_visualizer import NetworkVisualizer; print('✅ NetworkVisualizer import OK')"
	@$(PYTHON) -c "from utils.csv_handler import CSVHandler; print('✅ CSVHandler import OK')"
	@$(PYTHON) -c "from utils.path_finder import PathFinder; print('✅ PathFinder import OK')"
	@echo "$(GREEN)✅ All imports successful!$(NC)"

# Data management targets
.PHONY: check-data
check-data: ## Check data files exist and are valid
	@echo "$(BLUE)📊 Checking data files...$(NC)"
	@test -f $(DATA_DIR)/stations.csv || (echo "$(RED)❌ stations.csv not found$(NC)" && exit 1)
	@test -f $(DATA_DIR)/lines.csv || (echo "$(RED)❌ lines.csv not found$(NC)" && exit 1)
	@test -f $(DATA_DIR)/connections.csv || (echo "$(RED)❌ connections.csv not found$(NC)" && exit 1)
	@test -f $(DATA_DIR)/tickets.csv || (echo "$(RED)❌ tickets.csv not found$(NC)" && exit 1)
	@echo "$(GREEN)✅ All data files present$(NC)"

.PHONY: reset-data
reset-data: ## Reset ticket data (keep network data)
	@echo "$(YELLOW)⚠️  Resetting ticket data...$(NC)"
	@echo "ticket_id,origin_id,destination_id,price,path,instructions,purchase_date" > $(DATA_DIR)/tickets.csv
	@echo "$(GREEN)✅ Ticket data reset$(NC)"

.PHONY: backup-data
backup-data: ## Create backup of all data files
	@echo "$(BLUE)💾 Creating data backup...$(NC)"
	@mkdir -p backups
	@cp $(DATA_DIR)/*.csv backups/
	@echo "$(GREEN)✅ Data backed up to backups/$(NC)"

# Development targets
.PHONY: dev-setup
dev-setup: install check-data ## Complete development setup
	@echo "$(GREEN)🎉 Development environment ready!$(NC)"
	@echo "$(YELLOW)💡 Next steps:$(NC)"
	@echo "  make run     # Start the application"
	@echo "  make test    # Run tests"
	@echo "  make clean   # Clean up"

.PHONY: check-deps
check-deps: ## Check if dependencies are installed
	@echo "$(BLUE)🔍 Checking dependencies...$(NC)"
	@$(PYTHON) -c "import matplotlib, networkx" 2>/dev/null || (echo "$(RED)❌ Dependencies not installed. Run 'make install'$(NC)" && exit 1)
	@echo "$(GREEN)✅ Dependencies check passed$(NC)"

# Visualization targets
.PHONY: visualize
visualize: check-deps ## Generate and save network visualization
	@echo "$(BLUE)🎨 Generating network visualization...$(NC)"
	@$(PYTHON) -c "\
	from models.metro_network import MetroNetwork; \
	from visualization.network_visualizer import NetworkVisualizer; \
	metro = MetroNetwork(); \
	viz = NetworkVisualizer(metro); \
	viz.save_network_image('metro_network_map'); \
	print('✅ Network map saved as metro_network_map.png'); \
	"
	@echo "$(GREEN)✅ Visualization saved!$(NC)"

# Cleanup targets
.PHONY: clean
clean: ## Clean up temporary files
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	@rm -f *.pyc
	@rm -f */*.pyc
	@rm -f */*/*.pyc
	@rm -f .DS_Store
	@rm -f *.log
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

.PHONY: clean-all
clean-all: clean ## Clean everything including data
	@echo "$(YELLOW)⚠️  Cleaning all data...$(NC)"
	@rm -rf backups/
	@rm -f $(DATA_DIR)/tickets.csv
	@echo "ticket_id,origin_id,destination_id,price,path,instructions,purchase_date" > $(DATA_DIR)/tickets.csv
	@echo "$(GREEN)✅ Complete cleanup done$(NC)"

# Information targets
.PHONY: info
info: ## Show project information
	@echo "$(CYAN)🚇 Metro Ticket Purchasing System$(NC)"
	@echo "$(WHITE)================================$(NC)"
	@echo "$(YELLOW)Project:$(NC) $(PROJECT_NAME)"
	@echo "$(YELLOW)Python:$(NC) $$($(PYTHON) --version)"
	@echo "$(YELLOW)Main file:$(NC) $(MAIN_FILE)"
	@echo "$(YELLOW)Requirements:$(NC) $(REQUIREMENTS)"
	@echo "$(YELLOW)Data directory:$(NC) $(DATA_DIR)"
	@echo ""
	@echo "$(BLUE)📊 Data files:$(NC)"
	@ls -la $(DATA_DIR)/*.csv 2>/dev/null || echo "No data files found"
	@echo ""
	@echo "$(BLUE)📦 Dependencies:$(NC)"
	@$(PYTHON) -c "import matplotlib; print(f'matplotlib: {matplotlib.__version__}')" 2>/dev/null || echo "matplotlib: Not installed"
	@$(PYTHON) -c "import networkx; print(f'networkx: {networkx.__version__}')" 2>/dev/null || echo "networkx: Not installed"

.PHONY: status
status: check-deps check-data ## Show system status
	@echo "$(GREEN)✅ System Status: Ready$(NC)"
	@echo "$(BLUE)📊 Quick Stats:$(NC)"
	@$(PYTHON) -c "\
	from models.metro_network import MetroNetwork; \
	from models.ticket_manager import TicketManager; \
	metro = MetroNetwork(); \
	ticket_mgr = TicketManager(metro); \
	stats = metro.get_network_stats(); \
	print(f'  Stations: {stats[\"total_stations\"]}'); \
	print(f'  Lines: {stats[\"total_lines\"]}'); \
	print(f'  Interchanges: {stats[\"interchange_stations\"]}'); \
	print(f'  Tickets: {len(ticket_mgr.tickets)}'); \
	"

# Debug targets
.PHONY: debug
debug: ## Run with debug information
	@echo "$(BLUE)🐛 Running in debug mode...$(NC)"
	@PYTHONPATH=. $(PYTHON) -u $(MAIN_FILE)

.PHONY: lint
lint: ## Check code style (if flake8 is available)
	@echo "$(BLUE)🔍 Running code linting...$(NC)"
	@which flake8 > /dev/null 2>&1 && flake8 *.py */*.py || echo "$(YELLOW)⚠️  flake8 not installed, skipping linting$(NC)"

# Documentation targets
.PHONY: docs
docs: ## Generate documentation (if sphinx is available)
	@echo "$(BLUE)📚 Generating documentation...$(NC)"
	@which sphinx-build > /dev/null 2>&1 && echo "$(GREEN)✅ Sphinx available$(NC)" || echo "$(YELLOW)⚠️  Sphinx not installed$(NC)"

# All-in-one targets
.PHONY: setup
setup: install check-data test ## Complete setup and verification
	@echo "$(GREEN)🎉 Metro Ticket System is ready to use!$(NC)"
	@echo "$(YELLOW)💡 Run 'make run' to start the application$(NC)"

.PHONY: demo
demo: setup run ## Complete demo: setup and run
	@echo "$(GREEN)🎉 Demo completed!$(NC)"

# Special targets
.PHONY: .SILENT
.SILENT: help install run test clean info status

# Ensure targets run even if files exist
.PHONY: install-deps check-python check-deps check-data test-imports
