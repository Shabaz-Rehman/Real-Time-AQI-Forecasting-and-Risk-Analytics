#!/usr/bin/env python3
"""
Raspberry Pi AQI Gateway - Receiver
Real-Time Air Quality Monitoring System

Hardware:
- Raspberry Pi 4
- SX1276 LoRa Module

Author: [Your Name]
Date: 2025
"""

import json
import sqlite3
import time
import logging
from datetime import datetime
import threading
import board
import busio
import digitalio
import adafruit_rfm9x

# ===== CONFIGURATION =====
LORA_FREQUENCY = 915.0  # MHz (use 433.0 or 868.0 for other regions)
DATABASE_PATH = "aqi_data.db"
LOG_FILE = "receiver.log"

# LoRa GPIO Pins (BCM numbering)
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AQIReceiver:
    """AQI Gateway Receiver Class"""
    
    def __init__(self):
        """Initialize the receiver"""
        self.rfm9x = None
        self.db_conn = None
        self.running = False
        self.packets_received = 0
        self.packets_failed = 0
        
        logger.info("=" * 50)
        logger.info("AQI Gateway - Receiver")
        logger.info("=" * 50)
        
        # Initialize components
        self.init_database()
        self.init_lora()
        
    def init_database(self):
        """Initialize SQLite database"""
        try:
            logger.info("Initializing database...")
            
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # Create sensor_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp INTEGER NOT NULL,
                    node_id INTEGER NOT NULL,
                    packet_number INTEGER,
                    temperature REAL,
                    humidity REAL,
                    pm25 REAL,
                    pm10 REAL,
                    gas_level INTEGER,
                    smoke_level INTEGER,
                    aqi INTEGER,
                    rssi INTEGER,
                    snr REAL,
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON sensor_data(timestamp DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_node_id 
                ON sensor_data(node_id)
            ''')
            
            # Create statistics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    node_id INTEGER,
                    avg_aqi REAL,
                    max_aqi INTEGER,
                    min_aqi INTEGER,
                    avg_temp REAL,
                    avg_humidity REAL,
                    avg_pm25 REAL,
                    packets_received INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("✓ Database initialized successfully")
            
        except Exception as e:
            logger.error(f"✗ Database initialization failed: {e}")
            raise
    
    def init_lora(self):
        """Initialize LoRa radio"""
        try:
            logger.info("Initializing LoRa radio...")
            
            # Initialize SPI bus
            spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            
            # Initialize RFM9x
            self.rfm9x = adafruit_rfm9x.RFM9x(
                spi, CS, RESET, LORA_FREQUENCY
            )
            
            # Configure LoRa parameters (must match transmitter)
            self.rfm9x.tx_power = 23  # Max power
            self.rfm9x.spreading_factor = 12  # SF12 for long range
            self.rfm9x.signal_bandwidth = 125000  # 125 kHz
            self.rfm9x.coding_rate = 5  # 4/5
            self.rfm9x.enable_crc = True  # Enable CRC checking
            
            logger.info(f"✓ LoRa initialized at {LORA_FREQUENCY} MHz")
            logger.info(f"  Spreading Factor: {self.rfm9x.spreading_factor}")
            logger.info(f"  Bandwidth: {self.rfm9x.signal_bandwidth} Hz")
            logger.info(f"  TX Power: {self.rfm9x.tx_power} dBm")
            
        except Exception as e:
            logger.error(f"✗ LoRa initialization failed: {e}")
            raise
    
    def receive_packet(self):
        """Receive and process a LoRa packet"""
        try:
            # Check for packet with timeout
            packet = self.rfm9x.receive(timeout=5.0)
            
            if packet is None:
                return None
            
            # Convert bytes to string
            packet_text = str(packet, 'utf-8')
            
            # Get RSSI and SNR
            rssi = self.rfm9x.last_rssi
            snr = self.rfm9x.last_snr
            
            logger.info(f">>> Packet received (RSSI: {rssi} dBm, SNR: {snr} dB)")
            logger.info(f"    Data: {packet_text}")
            
            # Parse JSON
            try:
                data = json.loads(packet_text)
                data['rssi'] = rssi
                data['snr'] = snr
                return data
                
            except json.JSONDecodeError as e:
                logger.error(f"✗ JSON decode error: {e}")
                self.packets_failed += 1
                return None
                
        except Exception as e:
            logger.error(f"✗ Error receiving packet: {e}")
            return None
    
    def store_data(self, data):
        """Store received data in database"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sensor_data 
                (timestamp, node_id, packet_number, temperature, humidity, 
                 pm25, pm10, gas_level, smoke_level, aqi, rssi, snr)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('timestamp', 0),
                data.get('node_id', 0),
                data.get('packet', 0),
                data.get('temp', 0),
                data.get('humidity', 0),
                data.get('pm25', 0),
                data.get('pm10', 0),
                data.get('gas', 0),
                data.get('smoke', 0),
                data.get('aqi', 0),
                data.get('rssi', 0),
                data.get('snr', 0.0)
            ))
            
            conn.commit()
            conn.close()
            
            self.packets_received += 1
            
            logger.info(f"✓ Data stored (Node: {data.get('node_id')}, "
                       f"Packet: {data.get('packet')}, AQI: {data.get('aqi')})")
            
        except Exception as e:
            logger.error(f"✗ Error storing data: {e}")
            self.packets_failed += 1
    
    def display_statistics(self):
        """Display receiver statistics"""
        total = self.packets_received + self.packets_failed
        success_rate = (self.packets_received / total * 100) if total > 0 else 0
        
        logger.info("\n" + "=" * 50)
        logger.info("RECEIVER STATISTICS")
        logger.info("=" * 50)
        logger.info(f"Packets Received: {self.packets_received}")
        logger.info(f"Packets Failed: {self.packets_failed}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info("=" * 50 + "\n")
    
    def get_latest_data(self):
        """Get latest sensor reading from database"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT node_id, temperature, humidity, pm25, pm10, 
                       gas_level, smoke_level, aqi, rssi, snr, received_at
                FROM sensor_data 
                ORDER BY id DESC 
                LIMIT 1
            ''')
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'node_id': row[0],
                    'temperature': row[1],
                    'humidity': row[2],
                    'pm25': row[3],
                    'pm10': row[4],
                    'gas_level': row[5],
                    'smoke_level': row[6],
                    'aqi': row[7],
                    'rssi': row[8],
                    'snr': row[9],
                    'received_at': row[10]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting latest data: {e}")
            return None
    
    def display_latest_data(self):
        """Display latest sensor data"""
        data = self.get_latest_data()
        
        if data:
            logger.info("\n" + "=" * 50)
            logger.info("LATEST SENSOR DATA")
            logger.info("=" * 50)
            logger.info(f"Node ID: {data['node_id']}")
            logger.info(f"Temperature: {data['temperature']:.1f} °C")
            logger.info(f"Humidity: {data['humidity']:.1f} %")
            logger.info(f"PM2.5: {data['pm25']:.1f} µg/m³")
            logger.info(f"PM10: {data['pm10']:.1f} µg/m³")
            logger.info(f"Gas Level: {data['gas_level']}")
            logger.info(f"Smoke Level: {data['smoke_level']}")
            logger.info(f"AQI: {data['aqi']} ({self.get_aqi_category(data['aqi'])})")
            logger.info(f"Signal: RSSI {data['rssi']} dBm, SNR {data['snr']} dB")
            logger.info(f"Received: {data['received_at']}")
            logger.info("=" * 50 + "\n")
    
    def get_aqi_category(self, aqi):
        """Get AQI category from value"""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    def calculate_daily_statistics(self):
        """Calculate and store daily statistics"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # Get statistics for each node
            cursor.execute('''
                SELECT 
                    node_id,
                    AVG(aqi) as avg_aqi,
                    MAX(aqi) as max_aqi,
                    MIN(aqi) as min_aqi,
                    AVG(temperature) as avg_temp,
                    AVG(humidity) as avg_humidity,
                    AVG(pm25) as avg_pm25,
                    COUNT(*) as packet_count
                FROM sensor_data
                WHERE DATE(received_at) = ?
                GROUP BY node_id
            ''', (today,))
            
            stats = cursor.fetchall()
            
            for stat in stats:
                cursor.execute('''
                    INSERT OR REPLACE INTO statistics
                    (date, node_id, avg_aqi, max_aqi, min_aqi, avg_temp, 
                     avg_humidity, avg_pm25, packets_received)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (today, *stat))
            
            conn.commit()
            conn.close()
            
            logger.info(f"✓ Daily statistics calculated for {today}")
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
    
    def cleanup_old_data(self, days=30):
        """Remove data older than specified days"""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM sensor_data 
                WHERE received_at < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            
            if deleted > 0:
                logger.info(f"✓ Cleaned up {deleted} old records (>{days} days)")
                
        except Exception as e:
            logger.error(f"Error cleaning up data: {e}")
    
    def run(self):
        """Main receiver loop"""
        self.running = True
        
        logger.info("\n" + "=" * 50)
        logger.info("RECEIVER STARTED")
        logger.info("Listening for LoRa packets...")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 50 + "\n")
        
        stats_counter = 0
        cleanup_counter = 0
        
        try:
            while self.running:
                # Receive packet
                data = self.receive_packet()
                
                if data:
                    # Store in database
                    self.store_data(data)
                    
                    # Display every 10th packet
                    if self.packets_received % 10 == 0:
                        self.display_latest_data()
                
                # Display statistics every 50 packets
                stats_counter += 1
                if stats_counter >= 50:
                    self.display_statistics()
                    stats_counter = 0
                
                # Calculate daily stats and cleanup every 1000 packets
                cleanup_counter += 1
                if cleanup_counter >= 1000:
                    self.calculate_daily_statistics()
                    self.cleanup_old_data(days=30)
                    cleanup_counter = 0
                
        except KeyboardInterrupt:
            logger.info("\n\n" + "=" * 50)
            logger.info("RECEIVER STOPPED")
            logger.info("=" * 50)
            self.display_statistics()
            self.running = False

def main():
    """Main function"""
    try:
        # Create receiver instance
        receiver = AQIReceiver()
        
        # Start receiving
        receiver.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
