#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
import random
import string
import threading
from datetime import datetime
import os
import sys

# Custom color codes untuk terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class TerminalNGLSpammer:
    def __init__(self):
        self.is_running = False
        self.counter = 0
        self.stop_requested = False
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear')
    
    def print_banner(self):
        """Print fancy banner"""
        self.clear_screen()
        print(Colors.CYAN + Colors.BOLD)
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║    🚀 NGL SPAMMER PRO - by agusjawirtechid                  ║")
        print("║                                                              ║")
        print("║           Unlimited Messages • No Restrictions               ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(Colors.END)
        print(Colors.YELLOW + "💡 Tips: 'Unknown error from API' berarti PESAN BERHASIL TERKIRIM!")
        print("⚠️  Gunakan Ctrl+C untuk menghentikan spam" + Colors.END)
        print("=" * 65)
        print()
        
    def print_stats(self):
        """Print current statistics"""
        status = Colors.GREEN + "AKTIF" if self.is_running else Colors.RED + "TIDAK AKTIF"
        print("\n" + Colors.CYAN + "📊 STATISTICS:")
        print(Colors.WHITE + "  • Status: " + status)
        print("  • Pesan Terkirim: " + Colors.GREEN + str(self.counter))
        print("  • Target: " + Colors.YELLOW + getattr(self, 'current_username', 'N/A'))
        print("-" * 50 + Colors.END)
        
    def generate_device_id(self):
        """Generate random device ID"""
        return 'anon-' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9)) + str(int(time.time() * 1000))
    
    def extract_username(self, ngl_link):
        """Extract username dari URL NGL"""
        try:
            if ngl_link.endswith('/'):
                ngl_link = ngl_link[:-1]
            
            parts = ngl_link.split('/')
            username = parts[-1]
            
            if 'ngl.link' in username:
                username = parts[-2] if len(parts) > 2 else None
                
            return username
        except Exception as e:
            return None
    
    def send_message(self, ngl_link, message):
        """Kirim satu pesan ke NGL"""
        username = self.extract_username(ngl_link)
        if not username:
            return False, "Invalid NGL link"
        
        device_id = self.generate_device_id()
        
        data = {
            'username': username,
            'question': message,
            'deviceId': device_id,
            'gameSlug': '',
            'referrer': ''
        }
        
        try:
            response = requests.post(
                'https://ngl.link/api/submit',
                data=data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return True, "Pesan berhasil dikirim!"
                else:
                    error_msg = result.get('message', 'Unknown error from API')
                    if "Unknown error from API" in error_msg:
                        return True, "✅ BERHASIL! Terkirim ke " + username
                    else:
                        return False, error_msg
            else:
                return False, "HTTP Error: " + str(response.status_code)
                
        except Exception as e:
            return False, "Koneksi gagal: " + str(e)
    
    def get_user_input(self):
        """Dapatkan input dari user dengan styling"""
        print(Colors.GREEN + "🎯 MASUKKAN DETAIL SPAM:")
        print()
        
        ngl_link = input(Colors.CYAN + "🔗 NGL Link target " + Colors.WHITE + "(contoh: https://ngl.link/agus): " + Colors.YELLOW).strip()
        if not ngl_link:
            print(Colors.RED + "❌ URL tidak boleh kosong!")
            return None, None, None
        
        message = input(Colors.CYAN + "💬 Pesan yang akan dikirim: " + Colors.YELLOW).strip()
        if not message:
            print(Colors.RED + "❌ Pesan tidak boleh kosong!")
            return None, None, None
        
        delay_input = input(Colors.CYAN + "⚡ Delay (ms) " + Colors.WHITE + "[default: 1000]: " + Colors.YELLOW).strip()
        if not delay_input:
            delay = 1000
        else:
            try:
                delay = int(delay_input)
                if delay < 100:
                    print(Colors.RED + "❌ Delay minimal 100ms!")
                    return None, None, None
            except ValueError:
                print(Colors.RED + "❌ Delay harus berupa angka!")
                return None, None, None
        
        return ngl_link, message, delay
    
    def start_spamming(self, ngl_link, message, delay_ms):
        """Mulai proses spam"""
        self.is_running = True
        self.stop_requested = False
        self.counter = 0
        self.current_username = self.extract_username(ngl_link)
        
        print("\n" + Colors.GREEN + "🚀 MEMULAI SPAMMING...")
        print(Colors.CYAN + "🎯 Target: " + Colors.YELLOW + self.current_username)
        print(Colors.CYAN + "💬 Pesan: " + Colors.WHITE + message)
        print(Colors.CYAN + "⚡ Delay: " + Colors.WHITE + str(delay_ms) + "ms")
        print(Colors.CYAN + "⏰ Started at: " + Colors.WHITE + datetime.now().strftime('%H:%M:%S'))
        print("=" * 65 + Colors.END)
        
        try:
            while self.is_running and not self.stop_requested:
                self.counter += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # Kirim pesan
                success, status = self.send_message(ngl_link, message)
                
                # Tampilkan hasil dengan warna
                if success:
                    color = Colors.GREEN
                    icon = "✅"
                else:
                    color = Colors.RED
                    icon = "❌"
                
                print(color + icon + " [" + str(self.counter).zfill(3) + "] " + timestamp + " - " + status + Colors.END)
                
                # Update stats setiap 10 pesan
                if self.counter % 10 == 0:
                    self.print_stats()
                
                # Delay sebelum pesan berikutnya
                if not self.stop_requested:
                    time.sleep(delay_ms / 1000.0)
        
        except KeyboardInterrupt:
            print("\n" + Colors.YELLOW + "⚠️  Menghentikan spam..." + Colors.END)
            self.stop_requested = True
        
        # Tampilkan hasil akhir
        final_status = "DIHENTIKAN" if self.stop_requested else "SELESAI"
        final_color = Colors.YELLOW if self.stop_requested else Colors.GREEN
        
        print("=" * 65)
        print(final_color + "🏁 " + final_status + " - Total pesan terkirim: " + Colors.CYAN + str(self.counter))
        print(Colors.CYAN + "⏰ Finished at: " + Colors.WHITE + datetime.now().strftime('%H:%M:%S') + Colors.END)
        
        self.is_running = False
    
    def stop_spamming(self):
        """Hentikan proses spam"""
        if self.is_running:
            self.stop_requested = True

def main():
    spammer = TerminalNGLSpammer()
    
    try:
        while True:
            spammer.print_banner()
            
            # Dapatkan input user
            ngl_link, message, delay = spammer.get_user_input()
            if ngl_link is None:
                input("\n" + Colors.YELLOW + "⚠️  Tekan Enter untuk mencoba lagi..." + Colors.END)
                continue
            
            # Validasi username
            username = spammer.extract_username(ngl_link)
            if not username:
                print(Colors.RED + "❌ Link NGL tidak valid! Format: https://ngl.link/username")
                input("\n" + Colors.YELLOW + "⚠️  Tekan Enter untuk mencoba lagi..." + Colors.END)
                continue
            
            # Konfirmasi sebelum mulai
            print("\n" + Colors.YELLOW + "⚠️  KONFIRMASI:")
            print("   Target: " + Colors.CYAN + username)
            print("   Pesan: " + Colors.WHITE + message)
            print("   Delay: " + Colors.WHITE + str(delay) + "ms")
            
            confirm = input("\n" + Colors.GREEN + "🎯 Apakah Anda ingin memulai spam? (y/N): " + Colors.YELLOW).strip().lower()
            if confirm not in ['y', 'yes', 'ya']:
                print(Colors.YELLOW + "❌ Dibatalkan!")
                time.sleep(2)
                continue
            
            # Jalankan spam
            spammer.start_spamming(ngl_link, message, delay)
            
            # Tanya apakah ingin spam lagi
            print()
            restart = input(Colors.GREEN + "🔄 Apakah ingin spam lagi? (y/N): " + Colors.YELLOW).strip().lower()
            if restart not in ['y', 'yes', 'ya']:
                print("\n" + Colors.CYAN + "👋 Terima kasih telah menggunakan NGL Spammer Pro!" + Colors.END)
                break
            
    except KeyboardInterrupt:
        print("\n\n" + Colors.CYAN + "👋 Terima kasih telah menggunakan NGL Spammer Pro!" + Colors.END)
    except Exception as e:
        print("\n" + Colors.RED + "❌ Error: " + str(e))
        print(Colors.YELLOW + "⚠️  Program dihentikan karena error" + Colors.END)

if __name__ == "__main__":
    main()
