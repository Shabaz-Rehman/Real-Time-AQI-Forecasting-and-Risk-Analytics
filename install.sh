#!/bin/bash
#
# Air Quality Monitor - Raspberry Pi Installation Script
# This script automates the setup of the receiver on Raspberry Pi
#
# Usage: sudo bash install.sh
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "========================================="
echo " Air Quality Monitor - Installation"
echo "========================================="
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root: sudo bash install.sh${NC}"
    exit 1
fi

# Get the actual user (not root)
ACTUAL_USER=${SUDO_USER:-$USER}
USER_HOME=$(eval echo ~$ACTUAL_USER)

echo -e "${YELLOW}Installing for user: $ACTUAL_USER${NC}"
echo ""

# Step 1: Update system
echo -e "${GREEN}[1/8] Updating system...${NC}"
apt-get update
apt-get upgrade -y

# Step 2: Enable SPI
echo -e "${GREEN}[2/8] Enabling SPI interface...${NC}"
if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo "dtparam=spi=on" >> /boot/config.txt
    echo "SPI enabled (reboot required)"
else
    echo "SPI already enabled"
fi

# Step 3: Install system dependencies
echo -e "${GREEN}[3/8] Installing system dependencies...${NC}"
apt-get install -y \
    python3-pip \
    python3-dev \
    python3-spidev \
    python3-rpi.gpio \
    git \
    build-essential

# Step 4: Install Python packages
echo -e "${GREEN}[4/8] Installing Python packages...${NC}"
pip3 install --upgrade pip
pip3 install \
    spidev \
    RPi.GPIO \
    pandas \
    numpy \
    matplotlib \
    scikit-learn

# Step 5: Clone or update repository
echo -e "${GREEN}[5/8] Setting up project files...${NC}"
PROJECT_DIR="$USER_HOME/air_quality_project"

if [ -d "$PROJECT_DIR" ]; then
    echo "Project directory exists, updating..."
    cd "$PROJECT_DIR"
    git pull || echo "Not a git repository, skipping update"
else
    echo "Creating project directory..."
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# Create necessary directories
mkdir -p data logs backups

# Set permissions
chown -R $ACTUAL_USER:$ACTUAL_USER "$PROJECT_DIR"

# Step 6: Create configuration file
echo -e "${GREEN}[6/8] Creating configuration file...${NC}"
cat > "$PROJECT_DIR/config.py" << 'EOF'
# Air Quality Monitor Configuration

# LoRa Settings (MUST match ESP32)
LORA_FREQUENCY = 433E6  # 433 MHz
LORA_SYNC_WORD = 0x12
LORA_SPREADING_FACTOR = 7
LORA_BANDWIDTH = 125E3
LORA_CODING_RATE = 5

# File Paths
DATA_FILE = "data/air_quality_data.csv"
ALERT_FILE = "data/air_quality_alerts.log"
BACKUP_DIR = "backups"

# Alert Thresholds
ALERT_AQI_THRESHOLD = 150  # Alert when AQI > 150

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/receiver.log"
EOF

chown $ACTUAL_USER:$ACTUAL_USER "$PROJECT_DIR/config.py"

# Step 7: Test SPI
echo -e "${GREEN}[7/8] Testing SPI interface...${NC}"
if [ -e /dev/spidev0.0 ] && [ -e /dev/spidev0.1 ]; then
    echo -e "${GREEN}✓ SPI devices found${NC}"
else
    echo -e "${YELLOW}⚠ SPI devices not found. You may need to reboot.${NC}"
fi

# Step 8: Create systemd service (optional)
echo -e "${GREEN}[8/8] Setting up systemd service...${NC}"
read -p "Do you want to enable auto-start on boot? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cat > /etc/systemd/system/airquality.service << EOF
[Unit]
Description=Air Quality Monitor Receiver
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 $PROJECT_DIR/receiver_fixed.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable airquality.service
    echo -e "${GREEN}✓ Auto-start enabled${NC}"
    echo "  Start service: sudo systemctl start airquality"
    echo "  Stop service: sudo systemctl stop airquality"
    echo "  View logs: sudo journalctl -u airquality -f"
else
    echo "Skipping auto-start setup"
fi

# Installation complete
echo ""
echo -e "${GREEN}========================================="
echo " Installation Complete!"
echo "=========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Reboot if SPI was just enabled: sudo reboot"
echo "  2. Navigate to project: cd $PROJECT_DIR"
echo "  3. Run receiver: sudo python3 receiver_fixed.py"
echo ""
echo "For debugging: sudo python3 receiver_debug.py"
echo ""
echo -e "${YELLOW}Important: Make sure ESP32 is powered on and transmitting!${NC}"
echo ""

# Ask if user wants to reboot
if ! grep -q "^dtparam=spi=on" /boot/config.txt; then
    echo -e "${YELLOW}SPI was just enabled.${NC}"
    read -p "Reboot now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Rebooting in 5 seconds..."
        sleep 5
        reboot
    fi
fi

exit 0
