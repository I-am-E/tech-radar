import json,re
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from xml.etree import ElementTree as ET
FEEDS=[("The Verge","https://www.theverge.com/rss/index.xml","TECH"),("Ars Technica","https://feeds.arstechnica.com/arstechnica/index","TECH"),("MIT Technology Review","https://www.technologyreview.com/feed/","AI")]
def clean(s): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>","",s or "")).strip()
def fetch(name,url,category):
 root=ET.fromstring(urlopen(Request(url,headers={"User-Agent":"TechRadarBot/1.0"}),timeout=20).read())
 out=[]
 for item in root.findall(".//item")[:8]:
  title=clean(item.findtext("title"));link=clean(item.findtext("link"));desc=clean(item.findtext("description"))
  if title and link: out.append({"title":title,"summary":desc[:240] or "Fresh technology signal.","date":datetime.now(timezone.utc).date().isoformat(),"source":name,"category":category,"url":link})
 return out
try: old=json.load(open("posts.json",encoding="utf-8"))
except Exception: old=[]
seen={p.get("url") for p in old};new=[]
for feed in FEEDS:
 try:
  for p in fetch(*feed):
   if p["url"] not in seen: new.append(p);seen.add(p["url"])
 except Exception as e: print("feed failed:",feed[0],e)
if new:
 with open("posts.json","w",encoding="utf-8") as f: json.dump((new+old)[:60],f,ensure_ascii=False,indent=2)
 with open("CHANGELOG.md","a",encoding="utf-8") as f: f.write(f"\n- {datetime.now(timezone.utc).isoformat()} — Added {len(new)} fresh signals from public RSS feeds.\n")
 print("Added",len(new),"signals.")
else: print("No new signals.")
