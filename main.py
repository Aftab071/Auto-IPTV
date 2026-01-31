import requests
import re

url = "https://sonamul4545.vercel.app/siyam3535.m3u"

def check_link():
    print(f"Checking URL: {url}")
    try:
        # আমরা ব্রাউজারের মতো সেজে রিকোয়েস্ট পাঠাব
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Link is Working! Status 200 OK")
            lines = response.text.split('\n')
            count = 0
            print("\n--- First 10 Channels Found ---")
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    group_match = re.search(r'group-title="([^"]*)"', line)
                    name = line.split(',')[-1].strip()
                    group = group_match.group(1) if group_match else "No Group"
                    
                    print(f"Group: {group} | Name: {name}")
                    count += 1
                    if count >= 10: break # ১০টা দেখিয়ে থামবে
        else:
            print(f"Link Failed! Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_link()
