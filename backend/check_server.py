import requests
import time
import sys

def check_server_status():
    print("🔍 Checking server status...")
    
    # Test local server
    try:
        response = requests.get('http://localhost:8000/admin', timeout=5)
        if response.status_code == 200:
            print("✅ Local server is running on http://localhost:8000")
        else:
            print(f"⚠ Local server responded with status: {response.status_code}")
    except:
        print("❌ Local server is NOT running or not accessible")
        print("💡 Run: python manage.py runserver")
        return False
    
    # Test ngrok if available
    try:
        response = requests.get('http://localhost:4040/api/tunnels', timeout=2)
        tunnels = response.json()['tunnels']
        for tunnel in tunnels:
            if tunnel['proto'] == 'https':
                ngrok_url = tunnel['public_url']
                print(f"✅ Ngrok tunnel active: {ngrok_url}")
                
                # Test ngrok URL
                try:
                    ngrok_response = requests.get(f"{ngrok_url}/admin", timeout=5)
                    if ngrok_response.status_code == 200:
                        print("✅ Ngrok URL is accessible")
                    else:
                        print(f"⚠ Ngrok URL responded with: {ngrok_response.status_code}")
                except:
                    print("❌ Ngrok URL is NOT accessible")
                    
                return True
        print("❌ No active ngrok tunnels found")
        print("💡 Run: ngrok http 8000")
    except:
        print("❌ Ngrok is not running or not accessible")
        print("💡 Run: ngrok http 8000")
    
    return True

if __name__ == "__main__":
    check_server_status()