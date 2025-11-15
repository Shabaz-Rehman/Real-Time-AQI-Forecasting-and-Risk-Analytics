# Quick Start Guide

Get your Air Quality Monitor up and running in 15 minutes!

## 📦 What You Need

- ESP32 Development Board
- Raspberry Pi 3 (or newer)
- 2x LoRa RA-02 modules (433MHz)
- DHT11 sensor
- Dust sensor (PM2.5)
- SD card module
- Jumper wires

## 🚀 Quick Setup

### ESP32 (5 minutes)

1. **Connect Hardware**
   ```
   DHT11 → GPIO15 (with 10kΩ pull-up)
   LoRa MOSI → GPIO23
   LoRa MISO → GPIO19
   LoRa SCK → GPIO18
   LoRa NSS → GPIO5
   LoRa RESET → GPIO14
   LoRa DIO0 → GPIO2
   Dust Sensor → GPIO36
   ```

2. **Upload Code**
   ```
   - Open Arduino IDE
   - Install Libraries: LoRa, DHT sensor library
   - Open transmitter/esp32_transmitter.ino
   - Select Board: ESP32 Dev Module
   - Click Upload
   ```

3. **Verify**
   - Open Serial Monitor (115200 baud)
   - Should see "System Ready!" and transmission messages

### Raspberry Pi (10 minutes)

1. **Connect Hardware**
   ```
   LoRa VCC → Pin 1 (3.3V)
   LoRa GND → Pin 6
   LoRa MOSI → Pin 19
   LoRa MISO → Pin 21
   LoRa SCK → Pin 23
   LoRa NSS → Pin 24
   LoRa RESET → Pin 22
   LoRa DIO0 → Pin 18
   ```

2. **Run Installation**
   ```bash
   # Download and run installer
   wget https://raw.githubusercontent.com/yourusername/air-quality-monitor/main/scripts/install.sh
   sudo bash install.sh
   
   # Or manually:
   sudo apt-get update
   sudo raspi-config  # Enable SPI
   sudo pip3 install spidev RPi.GPIO
   git clone https://github.com/yourusername/air-quality-monitor.git
   cd air-quality-monitor/receiver
   ```

3. **Start Receiver**
   ```bash
   sudo python3 receiver_fixed.py
   ```

4. **Verify**
   - Should see "LISTENING FOR AIR QUALITY DATA"
   - Wait 30 seconds for ESP32 to transmit
   - Should receive packet with temperature, humidity, PM2.5, and AQI

## ✅ Testing

### Test 1: ESP32 Transmitter

**Expected Serial Monitor Output:**
```
========================================
ESP32 Air Quality Transmitter
========================================

Initializing DHT11... OK
Initializing LoRa... OK
  Frequency: 433 MHz
  Sync Word: 0x12
  Spreading Factor: 7

========== Sensor Readings ==========
Temperature: 25.3 °C
Humidity: 58.2 %
PM2.5: 32.4 µg/m³
AQI: 92 (Moderate)
=====================================

----- Transmitting -----
Packet: 0,25.3,58.2,32.4,92
✓ Transmission complete
```

### Test 2: Raspberry Pi Receiver

**Expected Terminal Output:**
```
============================================================
LISTENING FOR AIR QUALITY DATA
Frequency: 433 MHz | SF: 7 | BW: 125 kHz | Sync: 0x12
Press Ctrl+C to stop
============================================================

============================================================
PACKET: 12:30:45
Data: 0,25.3,58.2,32.4,92
RSSI: -45 dBm | SNR: 9.5 dB | Bytes: 19

✓ Msg #0
  Temperature: 25.3°C
  Humidity: 58.2%
  PM2.5: 32.4 µg/m³
  AQI: 92 (Moderate)
  Saved to air_quality_data.csv
Valid packets: 1
============================================================
```

## 🔧 Troubleshooting

### No packets received?

1. **Check distance**: Start with 1-2 meters apart
2. **Check antennas**: Must be connected to both LoRa modules
3. **Check frequency**: Both must be 433MHz (or 915MHz)
4. **Run debug**:
   ```bash
   sudo python3 receiver_debug.py
   ```

### ESP32 won't upload?

1. Hold BOOT button while uploading
2. Check USB cable (must support data)
3. Install CH340 driver if needed

### DHT11 shows NaN?

1. Add 10kΩ pull-up resistor between DATA and VCC
2. Wait 2 seconds after startup
3. Check wiring

### SD card not detected?

1. Format as FAT32
2. Try different SD card (32GB or smaller)
3. Check CS pin connection

## 📊 View Your Data

### Real-time on Raspberry Pi
```bash
# Watch live data
tail -f data/air_quality_data.csv
```

### Web Dashboard
```bash
cd dashboard
python3 -m http.server 8000
# Open: http://raspberrypi.local:8000
```

### Analytics
```bash
cd analytics
sudo python3 aqi_forecasting.py
# Generates reports and charts
```

## 🎯 Next Steps

1. **Extend Range**: Add external antennas
2. **Add Nodes**: Deploy multiple sensor nodes
3. **Set Alerts**: Configure email/SMS notifications
4. **Visualize**: Set up Grafana dashboard
5. **Forecast**: Enable ML-based predictions

## 📚 Full Documentation

- [README.md](README.md) - Complete documentation
- [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed setup
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues
- [API_REFERENCE.md](docs/API_REFERENCE.md) - API docs

## 🆘 Need Help?

- 📖 Check [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- 🐛 Open an issue on GitHub
- 💬 Join our community discussion

---

**Total Time**: ~15 minutes  
**Difficulty**: Beginner-Intermediate  
**Cost**: ~$50 in parts

Ready to breathe easier! 🌍💨
