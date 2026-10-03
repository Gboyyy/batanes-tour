from pathlib import Path
import urllib.request, re, html, concurrent.futures
from PIL import Image
from io import BytesIO
import json
entries = [(entry[2], entry[4]) for entry in json.loads(Path("scripts/gallery-destinations.json").read_text())]
def download(entry):
 slug, title = entry
 if (Path('public/photos') / (slug + '.webp')).exists(): return slug + ': already downloaded'
 page = 'https://commons.wikimedia.org/wiki/File:' + title
 request = urllib.request.Request(page, headers={'User-Agent':'BatanesDestinationGuide/1.0'})
 data = urllib.request.urlopen(request, timeout=30).read().decode()
 match = re.search(r'<div class="fullImageLink"[^>]*>.*?<a href="([^"]+)"', data, re.S)
 if not match: raise RuntimeError('Original image link not found for ' + title)
 url = html.unescape(match.group(1))
 raw = urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'BatanesDestinationGuide/1.0'}), timeout=45).read()
 image = Image.open(BytesIO(raw)).convert('RGB')
 image.thumbnail((1600,1600))
 target = Path('public/photos') / (slug + '.webp')
 image.save(target, 'WEBP', quality=86)
 return f'{slug}: {image.width} x {image.height}, {target.stat().st_size} bytes'
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
 for result in pool.map(download,entries): print(result)
