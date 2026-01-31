import requests
import re

# ==========================================
# আপনার ৪টি সোর্স লিংক
# ==========================================
source_urls = [
    "https://raw.githubusercontent.com/Aftab071/AftabIPTV/refs/heads/main/SyncIT",
    "https://raw.githubusercontent.com/sm-monirulislam/SM-Live-TV/refs/heads/main/Combined_Live_TV.m3u",
    "https://raw.githubusercontent.com/DrSujonPaul/Sujon/refs/heads/main/iptv",
    "https://sonamul4545.vercel.app/siyam3535.m3u"
]
# ==========================================

# প্লেলিস্টে গ্রুপের সিরিয়াল কেমন হবে
group_priority = [
    "Live Event",
    "Bangla",
    "Sports",
    "India",
    "Hindi",
    "Others"
]

def generate_playlist():
    specific_map = {}
    wildcard_map = {}
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # ১. my_channels.txt ফাইল পড়া
    try:
        with open("my_channels.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                parts = line.split("|")
                if len(parts) == 3:
                    src_group = parts[0].strip() 
                    src_name = parts[1].strip().lower()
                    target_group = parts[2].strip()

                    if src_name == "*":
                        wildcard_map[src_group] = target_group
                    else:
                        specific_map[(src_group, src_name)] = target_group
                    
    except FileNotFoundError:
        print("Error: 'my_channels.txt' file not found!")
        return

    print(f"Rules Loaded. Looking for groups like: {list(wildcard_map.keys())}")

    all_channels = []
    found_keys = set()
    found_links = set() # ডুপ্লিকেট লিংক আটকানোর জন্য

    # ২. সব সোর্স থেকে খোঁজা
    for url in source_urls:
        try:
            print(f"Scanning source: {url}")
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200:
                lines = response.text.split('\n')
                
                for i in range(len(lines)):
                    line = lines[i].strip()
                    
                    if line.startswith("#EXTINF"):
                        # গ্রুপ টাইটেল বের করা
                        group_match = re.search(r'group-title="([^"]*)"', line)
                        name_raw = line.split(',')[-1].strip()
                        
                        if group_match:
                            current_group = group_match.group(1).strip()
                            current_name = name_raw.strip().lower()
                            
                            new_target_group = None
                            
                            # === স্মার্ট চেকিং (Smart Match) ===
                            
                            # ১. নির্দিষ্ট নাম মিললে
                            if (current_group, current_name) in specific_map:
                                new_target_group = specific_map[(current_group, current_name)]
                            
                            # ২. ওয়াইল্ডকার্ড (*) চেকিং
                            else:
                                for w_group in wildcard_map:
                                    # যদি সোর্সের নামের ভেতরে আমাদের কিওয়ার্ড থাকে (যেমন: 'Bangla' শব্দটি 'Bangla🇧🇩' এর ভেতরে আছে)
                                    if w_group.lower() in current_group.lower():
                                        new_target_group = wildcard_map[w_group]
                                        break
                            
                            if new_target_group:
                                # লিংক বের করা
                                link_line = ""
                                if i + 1 < len(lines) and not lines[i+1].startswith("#"):
                                    link_line = lines[i+1].strip()
                                
                                # ডুপ্লিকেট চেকিং (একই লিংক যেন দুইবার না আসে)
                                if link_line and link_line not in found_links:
                                    modified_line = re.sub(r'group-title="[^"]*"', f'group-title="{new_target_group}"', line)
                                    
                                    all_channels.append({
                                        "group": new_target_group,
                                        "content": modified_line + "\n" + link_line + "\n"
                                    })
                                    found_links.add(link_line)
                                    
        except Exception as e:
            print(f"Error checking source: {e}")

    # ৩. সাজানো এবং সেভ করা
    def sort_key(channel):
        grp = channel["group"]
        if grp in group_priority:
            return group_priority.index(grp)
        return 999 

    all_channels.sort(key=sort_key)

    with open("my_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in all_channels:
            f.write(ch["content"])
    
    print(f"Success! Created my_playlist.m3u with {len(all_channels)} channels from {len(source_urls)} sources.")

if __name__ == "__main__":
    generate_playlist()
