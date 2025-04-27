# Car-Trace-Tracking
A Python application for tracking and analyzing vehicle movements using cellular network data. This project processes vehicle trace data to calculate movement patterns, speeds, and distances traveled.


## Overview
Car-Trace-Tracking analyzes vehicle location data based on cellular network identifiers (TMSI - Temporary Mobile Subscriber Identity). The system processes CSV data files containing location records to:
- Track vehicle movements over time
- Calculate distances between consecutive location points
- Determine travel speeds
- Identify maximum speeds and distances traveled
- Reverse geocode coordinates to readable addresses

## Features
- Load and process CSV data in efficient batches
- Track multiple vehicles simultaneously by their TMSI identifiers
- Calculate accurate distances between geographic coordinates
- Determine speed based on distance and time intervals
- Reverse geocode coordinates to human-readable addresses
- Handle errors gracefully with proper logging

## Installation
1. Clone the repository:
```shell
    git clone https://github.com/yourusername/Car-Trace-Tracking.git
    cd Car-Trace-Tracking
```

2. Set up a Python virtual environment (recommended):
```shell
   python -m venv .venv
   source .venv/bin/activate
```

3. Install the required dependencies:
```shell
   pip install -r requirements.txt
```

## Usage
### Basic Usage
Run the main application to process the default data file:

```shell
python car_trace.py
```

The application will:
1. Load data from the default file () `data/car-trace-large.csv`
2. Process the data to track vehicle movements
3. Output summary statistics about maximum speeds and distances

### Working with Different Data Files
To use a different data file:

### Input Data Format
The application expects CSV files with at least the following columns:
- : Timestamp in the format "YYYY-MM-DD HH:MM:SS" `end_time`
- : Vehicle identifier (Temporary Mobile Subscriber Identity) `m_tmsi`
- : Longitude coordinate `pos_last_lon`
- : Latitude coordinate `pos_last_lat`

## Project Structure
- : Main application logic for processing location data `car_trace.py`
- : Geographic utilities for distance calculations and reverse geocoding `agent.py`
- : Directory containing sample data files `data/`
- `tests/`: Unit tests for the application

## Testing
Run the test suite to verify functionality:

```shell
pytest
```

## Dependencies
- geopy: For geographic distance calculations and reverse geocoding
- geocoder: Alternative geocoding support
- pytest: For running the test suite
