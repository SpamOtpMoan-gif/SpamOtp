#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPAM OTP + REPOT - ENCRYPTED VERSION
# @makloYapitpp for Moan 🔐

import sys
import os
import base64
import subprocess
import platform
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# ================================================================
# 🔐 CEK LISENSI SEBELUM JALAN
# ================================================================

def get_hardware_id():
    try:
        if platform.system() == "Android":
            result = subprocess.run(['getprop', 'ro.serialno'], capture_output=True, text=True)
            if result.stdout.strip():
                return result.stdout.strip()
            result = subprocess.run(['getprop', 'ro.product.model'], capture_output=True, text=True)
            return result.stdout.strip()
        elif platform.system() == "Linux":
            result = subprocess.run(['cat', '/etc/machine-id'], capture_output=True, text=True)
            return result.stdout.strip()
        else:
            import wmi
            c = wmi.WMI()
            for system in c.Win32_ComputerSystemProduct():
                return system.UUID
    except:
        return "DEFAULT_HARDWARE_ID"

def generate_key():
    hardware_id = get_hardware_id()
    salt = b'spam_otp_encrypt_salt'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(hardware_id.encode()))
    return key

# ================================================================
# 🔐 DATA TERENKRIPSI (SPAM OTP CORE)
# ================================================================

ENCRYPTED_CORE = b"""
gAAAAABmS0yXbGVsbG8gdG9vbHMgc3BhbSBvdHAgZGFuIHJlcG9ydCB3aGF0c2FwcAog
QHByb2plY3QgaW5pIGRpYnVhdCBvbGVoIEBNYWtsb1lhcGl0dHBmb3IgTml0eURpenoK
VG9vbHMgdGVyZW5rcmlwc2kgZGFuIHRpZGFrIGJpc2EgZGljb2xvbmcgb3JhbmcgbGFpbg
"""

# ================================================================
# 🚀 DECRYPT & RUN
# ================================================================

try:
    key = generate_key()
    cipher = Fernet(key)
    
    # Decrypt core
    decrypted = cipher.decrypt(ENCRYPTED_CORE)
    
    # Eksekusi code
    exec(decrypted)
    
except Exception as e:
    print("""
╔═══════════════════════════════════════╗
║   ❌ ERROR!                           ║
║   TOOLS INI TIDAK VALID!              ║
║   HANYA UNTUK MONZAP!                 ║
╚═══════════════════════════════════════╝
    """)
    print(f"⚠️  ERROR: {str(e)}")
    print("💀 KALO MAU PAKE, BELI SENDIRI!")
    sys.exit(1)
