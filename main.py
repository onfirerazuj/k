#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TikTok OTP Sender Tool
Sends OTP to phone numbers from n.txt file
Skips already existing accounts
"""

import requests
import time
import sys
from phonenumbers import parse, is_valid_number
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

class TikTokOTPSender:
    def __init__(self):
        self.success_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.total_count = 0
        
    def read_numbers(self, filename='n.txt'):
        """Read phone numbers from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                numbers = [line.strip() for line in f if line.strip()]
            return numbers
        except FileNotFoundError:
            console.print(f"[red]Error: {filename} not found![/red]")
            return []
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            return []
    
    def validate_number(self, phone_number):
        """Validate phone number"""
        try:
            parsed = parse(phone_number, None)
            return is_valid_number(parsed)
        except:
            return False
    
    def check_existing_account(self, phone_number):
        """Check if account already exists on TikTok"""
        try:
            # TikTok API endpoint to check if user exists
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36'
            }
            
            # This is a simplified check - actual implementation may vary
            url = f"https://www.tiktok.com/api/user/search/"
            params = {
                'keywords': phone_number,
                'type': 1,
                'offset': 0,
                'count': 30,
                'from_user_id': 0,
                'user_id': 0
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            # If status code is 200 and user found, account exists
            if response.status_code == 200:
                data = response.json()
                if 'user_list' in data and len(data['user_list']) > 0:
                    return True
            return False
        except:
            return False
    
    def send_otp(self, phone_number):
        """Send OTP to phone number"""
        try:
            # Using a common OTP sending API
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36'
            }
            
            # TikTok OTP endpoint
            url = "https://www.tiktok.com/api/auth/phone/send_code/"
            
            data = {
                'phone_number': phone_number,
                'mix_mode': 1,
                'send_sm': 1
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status_code') == 0:
                    return True, "OTP sent successfully"
                else:
                    return False, result.get('status_msg', 'Failed to send OTP')
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Request timeout"
        except requests.exceptions.ConnectionError:
            return False, "Connection error"
        except Exception as e:
            return False, str(e)
    
    def process_numbers(self, numbers):
        """Process all phone numbers"""
        console.print("\n[bold cyan]TikTok OTP Sender Tool[/bold cyan]")
        console.print(f"[yellow]Total numbers found: {len(numbers)}[/yellow]\n")
        
        self.total_count = len(numbers)
        
        for i, number in enumerate(numbers, 1):
            console.print(f"\n[bold]{i}/{len(numbers)}[/bold] Processing: {number}")
            
            # Validate number
            if not self.validate_number(number):
                console.print(f"  [red]❌ Invalid phone number[/red]")
                self.failed_count += 1
                continue
            
            # Check if account exists
            console.print("  [yellow]🔍 Checking if account exists...[/yellow]")
            if self.check_existing_account(number):
                console.print(f"  [yellow]⏭️  Account already exists - Skipping[/yellow]")
                self.skipped_count += 1
                continue
            
            # Send OTP
            console.print("  [cyan]📱 Sending OTP...[/cyan]")
            success, message = self.send_otp(number)
            
            if success:
                console.print(f"  [green]✅ {message}[/green]")
                self.success_count += 1
            else:
                console.print(f"  [red]❌ {message}[/red]")
                self.failed_count += 1
            
            # Delay between requests to avoid rate limiting
            time.sleep(2)
    
    def print_summary(self):
        """Print summary table"""
        console.print("\n[bold]═══════════════════════════════════[/bold]")
        console.print("[bold cyan]📊 SUMMARY[/bold cyan]")
        console.print("[bold]═══════════════════════════════════[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Percentage", style="yellow")
        
        total = self.total_count if self.total_count > 0 else 1
        
        table.add_row(
            "✅ Success",
            str(self.success_count),
            f"{(self.success_count/total*100):.1f}%"
        )
        table.add_row(
            "❌ Failed",
            str(self.failed_count),
            f"{(self.failed_count/total*100):.1f}%"
        )
        table.add_row(
            "⏭️  Skipped",
            str(self.skipped_count),
            f"{(self.skipped_count/total*100):.1f}%"
        )
        table.add_row(
            "📊 Total",
            str(self.total_count),
            "100%"
        )
        
        console.print(table)
        console.print("\n[bold]═══════════════════════════════════[/bold]\n")

def main():
    """Main function"""
    try:
        sender = TikTokOTPSender()
        
        # Read numbers from file
        numbers = sender.read_numbers('n.txt')
        
        if not numbers:
            console.print("[red]No numbers found in n.txt[/red]")
            sys.exit(1)
        
        # Process numbers
        sender.process_numbers(numbers)
        
        # Print summary
        sender.print_summary()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Process interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
