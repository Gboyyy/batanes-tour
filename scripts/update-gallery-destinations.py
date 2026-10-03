from pathlib import Path
import json,re
from PIL import Image,ImageOps,ImageDraw
s=Path('src/App.jsx').read_text(encoding='utf-8')
entries=json.loads(Path('scripts/gallery-destinations.json').read_text())
lines=s.splitlines()
for index,title,slug,author,file,place in entries:
 assert (Path('public/photos')/(slug+'.webp')).exists(), slug
 lines[3+index]='  ['+json.dumps(title)+', `${import.meta.env.BASE_URL}photos/'+slug+'.webp`, '+json.dumps(author+' / Wikimedia Commons')+', '+json.dumps('https://commons.wikimedia.org/wiki/File:'+file)+', "https://creativecommons.org/licenses/by-sa/4.0/"],'
s='\n'.join(lines)+'\n'
s=s.replace('const photos = [', 'const heroPhoto = ["Coastal horizons", `${import.meta.env.BASE_URL}photos/gallery-0.webp`, "Traveloka / Shutterstock", "https://www.traveloka.com/en-ph/explore/destination/uncover-the-charm-of-batanes-acc/252986"]\nconst photos = [',1)
places=['Morong Beach, Sabtang','Tukon Chapel','Valugan Boulder Beach','Chawa View Deck','Alapad Rock Formation','House of Dakay, Ivana','San Carlos Borromeo Church, Mahatao','Dipnaysupuan Japanese Tunnel','Chamantad-Tinyan, Sabtang','Savidug, Sabtang','Rapang Cliffs, Itbayat','Vayang Rolling Hills','Basco Lighthouse','Rakuh a Payaman']
s=re.sub(r'const photoPlaces = .*', 'const photoPlaces = '+json.dumps(places),s)
s=s.replace('index === 8 || index === 9', 'index === 0 || index === 8 || index === 9')
s=s.replace("url('${photos[0][1]}')", "url('${heroPhoto[1]}')").replace('<PhotoCredit photo={photos[0]} className="hero-credit"/>','<PhotoCredit photo={heroPhoto} className="hero-credit"/>')
s=s.replace('All {photos.length} photographs.', '{photos.length} different places to discover.')
Path('src/App.jsx').write_text(s,encoding='utf-8')
paths=re.findall(r'photos/([^`]+\.webp)',s[s.index('const photos = ['):s.index('const photoPlaces')])
assert len(paths)==14 and len(set(paths))==14
canvas=Image.new('RGB',(1200,980),'white')
draw=ImageDraw.Draw(canvas)
titles=[json.loads(re.match(r'\s*\[(".*?"),',line)[1]) for line in s[s.index('const photos = ['):s.index('const photoPlaces')].splitlines() if line.strip().startswith('[')]
for i,name in enumerate(paths):
 with Image.open(Path('public/photos')/name) as image:
  canvas.paste(ImageOps.fit(image.convert('RGB'),(290,205)),((i%4)*300,(i//4)*245))
 draw.text(((i%4)*300+4,(i//4)*245+211),titles[i],fill='black')
canvas.save('scripts/gallery-review.jpg')
print('Gallery now contains 14 distinct destinations. Map searches and island stay links updated.')
