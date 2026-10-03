from pathlib import Path
import ast, urllib.request
from PIL import Image
from io import BytesIO
s=Path('src/App.jsx').read_text(encoding='utf-8')
photos=ast.literal_eval(s.split('const photos=',1)[1].split('\n',1)[0])
for index in [0,1,3,6,7]:
 target=Path('public/photos') / f'gallery-{index}.webp'
 try:
  if not target.exists():
   request=urllib.request.Request(photos[index][1],headers={'User-Agent':'Mozilla/5.0'})
   raw=urllib.request.urlopen(request,timeout=25).read()
   image=Image.open(BytesIO(raw)).convert('RGB')
   image.thumbnail((1800,1800))
   image.save(target,'WEBP',quality=86)
  print(f'Photo {index}: saved locally ({target.stat().st_size} bytes)')
 except Exception as error:
  print(f'Photo {index}: {error}')
