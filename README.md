# Real-Time Air Quality Index Forecasting and Risk Analytics

A complete IoT system for monitoring air quality using ESP32 and Raspberry Pi with LoRa communication. The system measures temperature, humidity, and PM2.5 levels to calculate real-time AQI (Air Quality Index) with risk analytics and forecasting capabilities.

![System Architecture](docs/architecture.png)

## 🌟 Features

- **Real-time Monitoring**: Continuous measurement of temperature, humidity, and PM2.5 particulate matter
- **Wireless Communication**: Long-range LoRa (433MHz) transmission up to 500m
- **AQI Calculation**: EPA-standard Air Quality Index calculation
- **Risk Analytics**: Automated health risk assessment and alerting
- **Data Logging**: CSV storage on SD card and Raspberry Pi
- **Forecasting**: Machine learning-based AQI prediction
- **Web Dashboard**: Real-time visualization with interactive charts

## 📋 Table of Contents

- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Hardware Requirements

### Transmitter (ESP32)
- ESP32 Development Board (ESP32 DevKit v1)
- DHT11 Temperature & Humidity Sensor
- GP2Y1010AU0F Dust Sensor (or compatible PM2.5 sensor)
- LoRa RA-02 SX1278 Module (433MHz)
- MicroSD Card Module
- MicroSD Card (8GB+, FAT32)
- Breadboard and jumper wires
- 10kΩ resistor (for DHT11 pull-up)
- 100nF capacitor (for LoRa VCC filtering)

### Receiver (Raspberry Pi)
- Raspberry Pi 3 Model B V1.2 (or newer)
- LoRa RA-02 SX1278 Module (433MHz)
- MicroSD Card (16GB+) with Raspberry Pi OS
- 5V 2.5A Power Supply

### Optional
- External antennas (3-5dBi) for extended range
- Weatherproof enclosures for outdoor deployment
- Solar panel + battery for remote installations

## 💻 Software Requirements

### ESP32
- Arduino IDE 2.0+
- ESP32 Board Support Package
- Libraries:
  - LoRa by Sandeep Mistry (v0.8.0+)
  - DHT sensor library by Adafruit (v1.4.4+)
  - Adafruit Unified Sensor (dependency)

### Raspberry Pi
- Raspberry Pi OS (Bullseye or newer)
- Python 3.7+
- Libraries:
  - spidev
  - RPi.GPIO
  - pandas (for analytics)
  - numpy
  - matplotlib
  - scikit-learn

## 🏗️ System Architecture

```
┌─────────────────┐                    ┌─────────────────┐
│   ESP32 Node    │                    │  Raspberry Pi   │
│                 │                    │                 │
│  ┌───────────┐  │                    │  ┌───────────┐  │
│  │   DHT11   │  │                    │  │   LoRa    │  │
│  └─────┬─────┘  │    LoRa 433MHz     │  │  RA-02    │  │
│        │        │◄──────────────────►│  └─────┬─────┘  │
│  ┌─────▼─────┐  │    (up to 500m)    │        │        │
│  │   ESP32   │  │                    │  ┌─────▼─────┐  │
│  │  MCU      │  │                    │  │    RPi    │  │
│  └─────┬─────┘  │                    │  │   SPI     │  │
│        │        │                    │  └─────┬─────┘  │
│  ┌─────▼─────┐  │                    │        │        │
│  │Dust Sensor│  │                    │  ┌─────▼─────┐  │
│  │ PM2.5     │  │                    │  │   Data    │  │
│  └───────────┘  │                    │  │ Storage   │  │
│                 │                    │  └───────────┘  │
│  ┌───────────┐  │                    │                 │
│  │ SD Card   │  │                    │  ┌───────────┐  │
│  │ Storage   │  │                    │  │   Web     │  │
│  └───────────┘  │                    │  │ Dashboard │  │
│                 │                    │  └───────────┘  │
└─────────────────┘                    └─────────────────┘
```

## 📥 Installation

### ESP32 Setup

1. **Install Arduino IDE**
   ```bash
   # Download from https://www.arduino.cc/en/software
   ```

2. **Add ESP32 Board Support**
   - Open Arduino IDE
   - Go to File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Tools → Board → Board Manager → Search "ESP32" → Install

3. **Install Required Libraries**
   - Tools → Manage Libraries
   - Install:
     - LoRa by Sandeep Mistry
     - DHT sensor library by Adafruit
     - Adafruit Unified Sensor

4. **Upload Firmware**
   ```bash
   # Open transmitter/esp32_transmitter.ino
   # Select Board: ESP32 Dev Module
   # Select Port: (your COM port)
   # Click Upload
   ```

### Raspberry Pi Setup

1. **Update System**
   ```bash
   sudo apt-get update
   sudo apt-get upgrade -y
   ```

2. **Enable SPI**
   ```bash
   sudo raspi-config
   # Interface Options → SPI → Enable
   sudo reboot
   ```

3. **Install Dependencies**
   ```bash
   sudo apt-get install -y python3-pip python3-dev git
   sudo pip3 install spidev RPi.GPIO pandas numpy matplotlib scikit-learn
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/air-quality-monitor.git
   cd air-quality-monitor
   ```

5. **Run Receiver**
   ```bash
   cd receiver
   sudo python3 receiver_fixed.py
   ```

## 🔌 Wiring Diagrams

### ESP32 Connections

| Component | Pin | ESP32 Pin | Notes |
|-----------|-----|-----------|-------|
| DHT11 VCC | VCC | 3.3V | Add 10kΩ pull-up resistor |
| DHT11 DATA | DATA | GPIO15 | Digital input |
| DHT11 GND | GND | GND | Common ground |
| LoRa VCC | VCC | 3.3V | Add 100nF capacitor |
| LoRa GND | GND | GND | Common ground |
| LoRa MOSI | MOSI | GPIO23 | SPI MOSI |
| LoRa MISO | MISO | GPIO19 | SPI MISO |
| LoRa SCK | SCK | GPIO18 | SPI Clock |
| LoRa NSS | NSS | GPIO5 | Chip select |
| LoRa RESET | RESET | GPIO14 | Reset pin |
| LoRa DIO0 | DIO0 | GPIO2 | Interrupt pin |
| SD Card VCC | VCC | 3.3V | Shared SPI |
| SD Card CS | CS | GPIO13 | Chip select |
| SD Card MOSI | MOSI | GPIO23 | Shared |
| SD Card MISO | MISO | GPIO19 | Shared |
| SD Card SCK | SCK | GPIO18 | Shared |
| Dust Sensor VCC | VCC | 5V | Requires 5V |
| Dust Sensor GND | GND | GND | Common ground |
| Dust Sensor Vo | Vo | GPIO36 | Analog input |

### Raspberry Pi Connections

| Component | Pin | RPi Pin | Notes |
|-----------|-----|---------|-------|
| LoRa VCC | VCC | Pin 1 (3.3V) | **3.3V ONLY** |
| LoRa GND | GND | Pin 6 (GND) | Common ground |
| LoRa MOSI | MOSI | Pin 19 (GPIO10) | SPI0 MOSI |
| LoRa MISO | MISO | Pin 21 (GPIO9) | SPI0 MISO |
| LoRa SCK | SCK | Pin 23 (GPIO11) | SPI0 SCK |
| LoRa NSS | NSS | Pin 24 (GPIO8) | SPI0 CE0 |
| LoRa RESET | RESET | Pin 22 (GPIO25) | Reset control |
| LoRa DIO0 | DIO0 | Pin 18 (GPIO24) | Interrupt |

## ⚙️ Configuration

### ESP32 Configuration

Edit `transmitter/esp32_transmitter.ino`:

```cpp
// Transmission interval (milliseconds)
#define SAMPLE_INTERVAL 30000  // 30 seconds

// LoRa frequency (must match receiver)
#define LORA_BAND 433E6  // 433 MHz

// LoRa parameters
#define LORA_SPREADING_FACTOR 7
#define LORA_BANDWIDTH 125E3
#define LORA_SYNC_WORD 0x12
```

### Raspberry Pi Configuration

Edit `receiver/receiver_fixed.py`:

```python
# LoRa configuration
FREQUENCY = 433E6  # Must match ESP32
SYNC_WORD = 0x12
SPREADING_FACTOR = 7

# File paths
DATA_FILE = "air_quality_data.csv"
ALERT_FILE = "air_quality_alerts.log"
```

## 🚀 Usage

### Starting the System

1. **Power on ESP32**
   - Connect via USB or external power
   - Open Serial Monitor (115200 baud) to view status

2. **Start Receiver**
   ```bash
   cd receiver
   sudo python3 receiver_fixed.py
   ```

3. **Monitor Data**
   - View real-time data on Serial Monitor (ESP32)
   - View received packets on Raspberry Pi terminal
   - Check CSV files for logged data

### Running Analytics

```bash
cd analytics
sudo python3 aqi_forecasting.py
```

This generates:
- Statistical analysis report
- AQI forecasting (next 6 hours)
- Visualization plots
- Alert logs

### Web Dashboard

```bash
cd dashboard
python3 -m http.server 8000
# Open browser: http://raspberrypi.local:8000
```

## 📊 Data Format

### Transmission Format (CSV)
```
message_count,temperature,humidity,pm25,aqi
0,25.3,58.2,32.4,92
```

### Stored Data Format
```csv
Timestamp,Msg#,Temp_C,Humidity_%,PM2.5,AQI,Risk,RSSI,SNR
2025-01-15 12:30:45,0,25.30,58.20,32.40,92,Moderate,-45,9.5
```

## 🎯 AQI Categories

| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0-50 | Good | Air quality is satisfactory |
| 51-100 | Moderate | Acceptable for most people |
| 101-150 | Unhealthy for Sensitive Groups | Sensitive groups may experience effects |
| 151-200 | Unhealthy | Everyone may experience effects |
| 201-300 | Very Unhealthy | Health alert conditions |
| 301-500 | Hazardous | Emergency conditions |

## 🐛 Troubleshooting

### ESP32 Issues

**LoRa initialization failed**
- Check wiring connections
- Verify 3.3V power supply
- Add 100nF capacitor between VCC and GND

**DHT11 reading NaN**
- Add 10kΩ pull-up resistor
- Check DATA pin connection
- Wait 2 seconds after startup

**SD card not detected**
- Format as FAT32
- Check CS pin (GPIO13)
- Try different SD card

### Raspberry Pi Issues

**No packets received**
- Verify SPI enabled: `ls /dev/spi*`
- Check LoRa wiring
- Reduce distance between devices
- Run debug version: `sudo python3 receiver_debug.py`

**Permission denied**
- Always run with `sudo`
- Add user to spi group: `sudo usermod -a -G spi,gpio pi`

**Import errors**
- Install missing libraries: `sudo pip3 install [library]`
- Check Python version: `python3 --version`

## 📈 Performance Metrics

- **Transmission Range**: 200-500m (line of sight)
- **Transmission Interval**: 30 seconds (configurable)
- **Packet Success Rate**: >95% at 100m
- **Power Consumption**: ~240mA TX, ~80mA idle (ESP32)
- **Battery Life**: ~12 hours (2000mAh battery)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- ESP32 community for hardware support
- Sandeep Mistry for LoRa library
- Adafruit for sensor libraries
- EPA for AQI calculation standards

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: your.email@example.com

## 🔮 Future Enhancements

- [ ] Multiple sensor nodes support
- [ ] MQTT integration for IoT platforms
- [ ] Mobile app (iOS/Android)
- [ ] Machine learning for predictive analytics
- [ ] GPS integration for location tracking
- [ ] Solar power support
- [ ] Weather API integration
- [ ] Email/SMS alerting system

---

**⭐ If you find this project useful, please star it on GitHub!**
