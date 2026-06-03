import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

CHAMPIONSHIPS_REGISTRY = [
    ("mundiais_longa", "mundial_longa2011.pdf", "http://www.omegatiming.com/File/Download?id=00010B0100FFFFFFFFFFFFFFFFFFFF20"),
    ("mundiais_longa", "mundial_longa2013.pdf", "http://www.omegatiming.com/File/Download?id=00010D0200FFFFFFFFFFFFFFFFFFFF20"),
    ("mundiais_longa", "mundial_longa2015.pdf", "http://www.omegatiming.com/File/Download?id=00010F0200FFFFFFFFFFFFFFFFFFFF20"),
    ("mundiais_curta", "mundial_curta2010.pdf", "http://www.omegatiming.com/File/Download?id=00010A0A00FFFFFFFFFFFFFFFFFFFF20"),
    ("mundiais_curta", "mundial_curta2012.pdf", "http://www.omegatiming.com/File/Download?id=00010C0100FFFFFFFFFFFFFFFFFFFF20"),
    ("mundiais_curta", "mundial_curta2014.pdf", "http://www.omegatiming.com/File/Download?id=00010E010DFFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_longa", "europeu_longa2020.pdf", "http://budapest2020.microplustiming.com/export/NU_Budapest2021/NU/pdf/Book.pdf"),
    ("continentais_curta", "europeu_curta2010.pdf", "http://www.omegatiming.com/File/Download?id=00010A0100FFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2011.pdf", "http://www.omegatiming.com/File/Download?id=00010B0300FFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2012.pdf", "http://www.omegatiming.com/File/Download?id=00010C0200FFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2013.pdf", "http://www.omegatiming.com/File/Download?id=00010D0100FFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2015.pdf", "http://www.omegatiming.com/File/Download?id=00010F0100FFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2017.pdf", "http://www.omegatiming.com/File/Download?id=000111010AFFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2019.pdf", "http://www.omegatiming.com/File/Download?id=000113010DFFFFFFFFFFFFFFFFFFFF20"),
    ("continentais_curta", "europeu_curta2021.pdf", "http://www.omegatiming.com/File/Download?id=0001150001FFFFFFFFFFFFFFFFFFFF20")
]

PDFS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pdfs_omega"))

import time

def download_item(item):
    category, file_name, url = item
    dest_path = os.path.join(PDFS_ROOT, category, file_name)
    
    # If file already exists and is valid size, skip
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"Skipping {file_name} (already exists)")
        return True
        
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    
    max_retries = 3
    retry_delay = 3.0
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(dest_path, "wb") as f:
                    f.write(response.read())
            print(f"Downloaded {file_name} successfully")
            return True
        except Exception as e:
            print(f"Attempt {attempt} failed for {file_name}: {e}")
            if os.path.exists(dest_path):
                os.remove(dest_path)
            if attempt < max_retries:
                time.sleep(retry_delay)
    return False

def main():
    print("Starting controlled parallel downloads...")
    # Use only 2 workers to avoid triggering Omega Timing's firewall
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(download_item, CHAMPIONSHIPS_REGISTRY))
    success = sum(1 for r in results if r)
    print(f"Done! {success}/{len(CHAMPIONSHIPS_REGISTRY)} downloads completed.")

if __name__ == "__main__":
    main()
