#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TARGET MANAGEMENT - VERSION 2.0
# @makloYapitpp for Mosn 💮

import json
import os
import re
from datetime import datetime

TARGETS_FILE = "targets.json"
BACKUP_FILE = "targets_backup.json"

# ================================================================
# 📱 FUNGSI TARGET
# ================================================================

def load_targets():
    """Load targets dari file"""
    try:
        if os.path.exists(TARGETS_FILE):
            with open(TARGETS_FILE, "r") as f:
                data = json.load(f)
                # Format baru: list of dict
                if isinstance(data, list) and all(isinstance(i, dict) for i in data):
                    return data
                # Format lama: list of string
                elif isinstance(data, list):
                    return [{"phone": p, "added": datetime.now().isoformat(), "status": "active"} for p in data]
                return []
    except:
        return []
    return []

def save_targets(targets):
    """Save targets ke file"""
    try:
        with open(TARGETS_FILE, "w") as f:
            json.dump(targets, f, indent=2)
        return True
    except:
        return False

def get_targets():
    """Dapatkan semua target (format sederhana)"""
    targets = load_targets()
    return [t.get("phone") if isinstance(t, dict) else t for t in targets]

def get_targets_full():
    """Dapatkan semua target (format lengkap)"""
    return load_targets()

def add_target(phone):
    """Tambah target"""
    phone = format_phone(phone)
    if not validate_phone(phone):
        return False
    
    targets = load_targets()
    # Cek duplikat
    existing = [t for t in targets if t.get("phone") == phone]
    if existing:
        return False
    
    targets.append({
        "phone": phone,
        "added": datetime.now().isoformat(),
        "status": "active",
        "attempts": 0,
        "success": 0
    })
    return save_targets(targets)

def remove_target(phone):
    """Hapus target"""
    phone = format_phone(phone)
    targets = load_targets()
    new_targets = [t for t in targets if t.get("phone") != phone]
    if len(new_targets) == len(targets):
        return False
    return save_targets(new_targets)

def clear_targets():
    """Hapus semua target"""
    return save_targets([])

def target_count():
    """Jumlah target"""
    return len(load_targets())

def get_active_targets():
    """Dapatkan target aktif"""
    targets = load_targets()
    return [t for t in targets if t.get("status") == "active"]

def get_inactive_targets():
    """Dapatkan target non-aktif"""
    targets = load_targets()
    return [t for t in targets if t.get("status") != "active"]

def update_target_status(phone, status):
    """Update status target"""
    phone = format_phone(phone)
    targets = load_targets()
    for t in targets:
        if t.get("phone") == phone:
            t["status"] = status
            return save_targets(targets)
    return False

def increment_attempt(phone):
    """Increment attempt count"""
    phone = format_phone(phone)
    targets = load_targets()
    for t in targets:
        if t.get("phone") == phone:
            t["attempts"] = t.get("attempts", 0) + 1
            return save_targets(targets)
    return False

def increment_success(phone):
    """Increment success count"""
    phone = format_phone(phone)
    targets = load_targets()
    for t in targets:
        if t.get("phone") == phone:
            t["success"] = t.get("success", 0) + 1
            return save_targets(targets)
    return False

def backup_targets():
    """Backup targets"""
    targets = load_targets()
    try:
        with open(BACKUP_FILE, "w") as f:
            json.dump({
                "backup_date": datetime.now().isoformat(),
                "targets": targets
            }, f, indent=2)
        return True
    except:
        return False

def restore_targets():
    """Restore targets dari backup"""
    try:
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, "r") as f:
                data = json.load(f)
                return save_targets(data.get("targets", []))
        return False
    except:
        return False

def format_phone(phone):
    """Format nomor telepon"""
    # Hapus karakter non-digit
    phone = re.sub(r'[^0-9]', '', phone)
    
    # Tambahkan 62 jika tidak ada
    if not phone.startswith('62'):
        if phone.startswith('0'):
            phone = '62' + phone[1:]
        else:
            phone = '62' + phone
    
    return phone

def validate_phone(phone):
    """Validasi nomor telepon"""
    phone = format_phone(phone)
    return len(phone) >= 10 and len(phone) <= 15

def get_target_stats():
    """Dapatkan statistik target"""
    targets = load_targets()
    if not targets:
        return {"total": 0, "active": 0, "inactive": 0, "total_attempts": 0, "total_success": 0}
    
    stats = {
        "total": len(targets),
        "active": len([t for t in targets if t.get("status") == "active"]),
        "inactive": len([t for t in targets if t.get("status") != "active"]),
        "total_attempts": sum(t.get("attempts", 0) for t in targets),
        "total_success": sum(t.get("success", 0) for t in targets)
    }
    return stats

def import_targets_from_file(filename):
    """Import targets dari file"""
    try:
        if not os.path.exists(filename):
            return False
        
        with open(filename, "r") as f:
            content = f.read()
        
        # Support berbagai format
        phones = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                # Ambil nomor dari teks
                numbers = re.findall(r'\d{10,15}', line)
                for num in numbers:
                    phones.append(format_phone(num))
        
        if not phones:
            return False
        
        targets = load_targets()
        existing_phones = [t.get("phone") for t in targets]
        
        for phone in phones:
            if phone not in existing_phones:
                targets.append({
                    "phone": phone,
                    "added": datetime.now().isoformat(),
                    "status": "active",
                    "attempts": 0,
                    "success": 0
                })
        
        return save_targets(targets)
    except:
        return False

def export_targets_to_file(filename="targets_export.txt"):
    """Export targets ke file"""
    targets = get_targets()
    if not targets:
        return False
    
    try:
        with open(filename, "w") as f:
            f.write(f"# TARGETS EXPORT - {datetime.now().isoformat()}\n")
            f.write(f"# TOTAL: {len(targets)}\n\n")
            for t in targets:
                f.write(f"{t}\n")
        return True
    except:
        return False
