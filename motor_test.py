#!/usr/bin/env python3
"""
REV Expansion Hub - Motor Test Script
Run on Raspberry Pi with hub connected via Mini USB.

Install dependency first:
  pip3 install pyserial

Add yourself to dialout group (then log out/in):
  sudo usermod $USER -a -G dialout
"""

import serial
import struct
import time

# ── Config ────────────────────────────────────────────────────────────────────
PORT      = "/dev/ttyUSB0"   # Change to /dev/ttyUSB0 if ACM0 doesn't appear
BAUD      = 460800
HUB_ADDR  = 0                # Default hub address

# ── REV Hub Serial Protocol helpers ───────────────────────────────────────────
SYNC_BYTES = bytes([0x44, 0x4F])

def checksum(data: bytes) -> int:
    return (~sum(data)) & 0xFF

def build_packet(msg_num: int, packet_type_id: int, payload: bytes) -> bytes:
    """Build a REV Hub serial packet."""
    header = struct.pack('<BBBBBB',
        0x44, 0x4F,          # Sync
        HUB_ADDR,            # Destination (hub address)
        0xFF,                # Source (host)
        packet_type_id,      # Packet type
        len(payload) + 1     # Payload length + checksum byte
    )
    msg_byte = struct.pack('<B', msg_num & 0xFF)
    body = msg_byte + payload
    chk = checksum(header[2:] + body)
    return header + body + bytes([chk])

def set_motor_mode(ser, msg_num, channel, mode=2):
    """
    Set motor to run mode.
    mode=0: Stop, mode=1: Constant power, mode=2: Float
    Packet type 0x73 = SetMotorChannelMode
    """
    payload = struct.pack('<BB', channel, mode)
    pkt = build_packet(msg_num, 0x73, payload)
    ser.write(pkt)
    time.sleep(0.05)
    ser.read(ser.in_waiting)  # flush response

def set_motor_power(ser, msg_num, channel, power):
    """
    Set motor power.
    power range: -32767 to 32767 (0 = stop, 32767 = full forward)
    Packet type 0x74 = SetMotorConstantPower
    """
    payload = struct.pack('<Bh', channel, power)
    pkt = build_packet(msg_num, 0x74, payload)
    ser.write(pkt)
    time.sleep(0.05)
    ser.read(ser.in_waiting)  # flush response

# ── Main test ─────────────────────────────────────────────────────────────────
def run_test():
    print(f"Connecting to REV Expansion Hub on {PORT}...")
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        time.sleep(0.5)  # Let hub wake up
        print("Connected!\n")

        msg = 0  # Rolling message counter

        for channel in range(4):  # Test all 4 motor channels
            print(f"--- Motor channel {channel} ---")

            # Set to constant power mode
            set_motor_mode(ser, msg, channel, mode=1)
            msg += 1

            print(f"  Forward 50%...")
            set_motor_power(ser, msg, channel, 16383)   # ~50% forward
            msg += 1
            time.sleep(2)

            print(f"  Stop.")
            set_motor_power(ser, msg, channel, 0)
            msg += 1
            time.sleep(0.5)

            print(f"  Reverse 50%...")
            set_motor_power(ser, msg, channel, -16383)  # ~50% reverse
            msg += 1
            time.sleep(2)

            print(f"  Stop.\n")
            set_motor_power(ser, msg, channel, 0)
            msg += 1
            time.sleep(0.5)

        print("Test complete!")

if __name__ == "__main__":
    run_test()