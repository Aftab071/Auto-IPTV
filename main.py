import requests
import re

# যে লিংকের সব চ্যানেলের নাম দেখতে চান, সেটি এখানে দিন
url = "https://sonamul4545.vercel.app/siyam3535.m3u"

def get_all_channel_names():
    print(f"Connecting to: {url} ...")
    try:
        # ব্রাউজারের মতো রিকোয়েস্ট পাঠানো (যাতে ব্লক না খায়)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            lines = response.text.split('\n')
            print("\n" + "="*50)
            print(" COPY FROM BELOW AND PASTE IN YOUR FILE ")
            print("="*50 + "\n")
            
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    # ১. গ্রুপের নাম বের করা
                    group_match = re.search(r'group-title="([^"]*)"', line)
                    group = group_match.group(1) if group_match else "No Group"
                    
                    # ২. চ্যানেলের নাম বের করা (কমার পরের অংশ)
                    name = line.split(',')[-1].strip()
                    
                    # ৩. প্রিন্ট করা (আপনার my_channels.txt এর ফরম্যাটে)
                    # এখানে আমি ডিফল্টভাবে 'Bangla' গ্রুপ দিয়ে দিচ্ছি, আপনি পরে চাইলে বদলাতে পারেন
                    print(f"{group} | {name} | Bangla")
            
            print("\n" + "="*50)
            print(" END OF LIST ")
            print("="*50 + "\n")
            
        else:
            print(f"Link failed! Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_all_channel_names()
