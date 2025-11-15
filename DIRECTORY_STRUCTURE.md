# Project Directory Structure

```
air-quality-monitor/
│
├── README.md                          # Main project documentation
├── LICENSE                            # MIT License
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # Python dependencies
│
├── docs/                              # Documentation
│   ├── architecture.png               # System architecture diagram
│   ├── wiring-esp32.png              # ESP32 wiring diagram
│   ├── wiring-raspberry-pi.png       # Raspberry Pi wiring diagram
│   ├── SETUP_GUIDE.md                # Detailed setup instructions
│   ├── TROUBLESHOOTING.md            # Troubleshooting guide
│   └── API_REFERENCE.md              # API documentation
│
├── transmitter/                       # ESP32 transmitter code
│   ├── esp32_transmitter/
│   │   ├── esp32_transmitter.ino     # Main Arduino sketch
│   │   ├── config.h                  # Configuration file
│   │   └── sensors.h                 # Sensor functions
│   └── README.md                     # Transmitter documentation
│
├── receiver/                          # Raspberry Pi receiver code
│   ├── receiver_fixed.py             # Main receiver (production)
│   ├── receiver_debug.py             # Debug version
│   ├── receiver_polling.py           # Alternative polling method
│   ├── config.py                     # Configuration settings
│   └── README.md                     # Receiver documentation
│
├── analytics/                         # Data analysis and forecasting
│   ├── aqi_forecasting.py            # AQI prediction script
│   ├── data_analysis.py              # Statistical analysis
│   ├── visualization.py              # Plotting functions
│   └── README.md                     # Analytics documentation
│
├── dashboard/                         # Web dashboard
│   ├── index.html                    # Main HTML file
│   ├── css/
│   │   └── style.css                 # Stylesheet
│   ├── js/
│   │   ├── app.js                    # Main JavaScript
│   │   └── charts.js                 # Chart configurations
│   └── README.md                     # Dashboard documentation
│
├── scripts/                           # Utility scripts
│   ├── install.sh                    # Installation script
│   ├── setup_autostart.sh            # Auto-start configuration
│   ├── backup_data.sh                # Data backup script
│   └── test_connection.py            # Connection test utility
│
├── data/                              # Data storage (gitignored)
│   ├── air_quality_data.csv          # Received data
│   ├── air_quality_alerts.log        # Alert logs
│   └── backups/                      # Data backups
│
├── tests/                             # Unit tests
│   ├── test_transmitter.cpp          # ESP32 tests
│   ├── test_receiver.py              # Receiver tests
│   └── test_analytics.py             # Analytics tests
│
└── examples/                          # Example usage
    ├── basic_usage.md                # Basic usage examples
    ├── advanced_config.md            # Advanced configuration
    └── integration_examples.md       # Integration with other systems
```

## File Descriptions

### Root Files

- **README.md**: Main project documentation with overview, installation, and usage
- **LICENSE**: MIT License for open-source distribution
- **.gitignore**: Specifies files to ignore in version control
- **requirements.txt**: Python package dependencies for Raspberry Pi

### Documentation (/docs)

- **architecture.png**: Visual diagram of system architecture
- **wiring-*.png**: Detailed wiring diagrams for both devices
- **SETUP_GUIDE.md**: Step-by-step setup instructions
- **TROUBLESHOOTING.md**: Common issues and solutions
- **API_REFERENCE.md**: API documentation for programmatic access

### Transmitter (/transmitter)

- **esp32_transmitter.ino**: Main Arduino code for ESP32
- **config.h**: Configuration constants and settings
- **sensors.h**: Sensor reading and processing functions

### Receiver (/receiver)

- **receiver_fixed.py**: Production-ready receiver using direct SPI
- **receiver_debug.py**: Debug version with verbose output
- **receiver_polling.py**: Alternative implementation using polling
- **config.py**: Configuration file for receiver settings

### Analytics (/analytics)

- **aqi_forecasting.py**: Time-series forecasting for AQI prediction
- **data_analysis.py**: Statistical analysis and reporting
- **visualization.py**: Data visualization and plotting utilities

### Dashboard (/dashboard)

- **index.html**: Web-based dashboard for real-time monitoring
- **style.css**: Dashboard styling
- **app.js**: Dashboard logic and data fetching
- **charts.js**: Chart.js configurations for visualizations

### Scripts (/scripts)

- **install.sh**: Automated installation for Raspberry Pi
- **setup_autostart.sh**: Configure system to start on boot
- **backup_data.sh**: Automated data backup utility
- **test_connection.py**: Test LoRa connectivity

### Tests (/tests)

- **test_transmitter.cpp**: Unit tests for ESP32 functions
- **test_receiver.py**: Unit tests for receiver functionality
- **test_analytics.py**: Tests for analytics algorithms

### Examples (/examples)

- **basic_usage.md**: Simple usage examples
- **advanced_config.md**: Advanced configuration scenarios
- **integration_examples.md**: Integration with IoT platforms

## Data Flow

```
ESP32 Sensors → ESP32 MCU → LoRa TX
                                ↓
                          (433 MHz Radio)
                                ↓
                            LoRa RX → Raspberry Pi SPI
                                         ↓
                                    Data Processing
                                         ↓
                        ┌────────────────┼────────────────┐
                        ↓                ↓                ↓
                   CSV Storage    Analytics/ML      Web Dashboard
```

## Setup Order

1. Clone repository
2. Set up transmitter (ESP32)
3. Set up receiver (Raspberry Pi)
4. Test basic communication
5. Configure analytics (optional)
6. Set up web dashboard (optional)
7. Configure auto-start (optional)

## Deployment

For production deployment:
1. Use `receiver_fixed.py` (most stable)
2. Enable auto-start with systemd
3. Set up data backup scripts
4. Configure alerts for unhealthy AQI
5. Use external antennas for better range
