import requests
import re

# ==========================================
# আপনার সোর্স লিংক
# ==========================================
source_urls = [
    "https://sonamul4545.vercel.app/siyam3535.m3u",
    # আপনার অন্য কোনো লিংক থাকলে এখানে দিন, না থাকলে এই লাইন মুছে দিন
]
# ==========================================

# আপনার পছন্দের সিরিয়াল
group_priority = [
    "Live Event",
    "Bangla",
]

def generate_playlist():
    specific_map = {}
    wildcard_map = {}
    
    # Header যোগ করা হলো যাতে সার্ভার ব্লক না করে
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
                    src_group = parts[0].strip().lower()
                    src_name = parts[1].strip().lower()
                    target_group = parts[2].strip()

                    if src_name == "*":
                        wildcard_map[src_group] = target_group
                    else:
                        specific_map[(src_group, src_name)] = target_group
                    
    except FileNotFoundError:
        print("Error: 'my_channels.txt' file not found!")
        return

    print(f"Tracking {len(specific_map)} specific channels and {len(wildcard_map)} dynamic groups.")

    all_channels = []
    found_keys = set()

    # ২. সোর্স থেকে খোঁজা
    for url in source_urls:
        try:
            print(f"Scanning source: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                lines = response.text.split('\n')
                
                for i in range(len(lines)):
                    line = lines[i].strip()
                    
                    if line.startswith("#EXTINF"):
                        group_match = re.search(r'group-title="([^"]*)"', line)
                        name_raw = line.split(',')[-1].strip()
                        
                        if group_match and name_raw:
                            current_group = group_match.group(1).strip().lower()
                            current_name = name_raw.strip().lower()
                            
                            new_target_group = None
                            
                            # চেক: নির্দিষ্ট চ্যানেল নাকি ওয়াইল্ডকার্ড?
                            if (current_group, current_name) in specific_map:
                                new_target_group = specific_map[(current_group, current_name)]
                            elif current_group in wildcard_map:
                                new_target_group = wildcard_map[current_group]
                            
                            if new_target_group:
                                unique_key = (current_group, current_name, new_target_group)
                                
                                if unique_key not in found_keys:
                                    # গ্রুপ নাম পরিবর্তন
                                    modified_line = re.sub(r'group-title="[^"]*"', f'group-title="{new_target_group}"', line)
                                    
                                    # লিংকের লাইন বের করা
                                    link_line = ""
                                    if i + 1 < len(lines) and not lines[i+1].startswith("#"):
                                        link_line = lines[i+1].strip()
                                    
                                    if link_line:
                                        all_channels.append({
                                            "group": new_target_group,
                                            "content": modified_line + "\n" + link_line + "\n"
                                        })
                                        found_keys.add(unique_key)
                                    
        except Exception as e:
            print(f"Error checking source: {e}")

    # ৩. সাজানো (Sorting)
    def sort_key(channel):
        grp = channel["group"]
        if grp in group_priority:
            return group_priority.index(grp)
        return 999 

    all_channels.sort(key=sort_key)

    # ৪. ফাইল সেভ করা (এটিই আপনার ডিলিট হওয়া ফাইল ফিরিয়ে আনবে)
    with open("my_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in all_channels:
            f.write(ch["content"])
    
    print(f"Success! Created my_playlist.m3u with {len(all_channels)} channels.")

if __name__ == "__main__":
    generate_playlist()
