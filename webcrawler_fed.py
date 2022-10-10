from bs4 import BeautifulSoup
import urllib.request
seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

# Draw hidden seed url from sample childurls
# (for example: the latest release https://www.federalreserve.gov/newsevents/pressreleases/bcreg20221006a.htm)
# and rewrite the seed_url match the format for later comparison:
hseed_url = "https://www.federalreserve.gov/newsevents/pressreleases/"

urls = [seed_url] 
seen = [seed_url]
opened = []
targetUrls = []
outNumUrl = 20 # output at least 10 urls

print("Starting with url = " + str(urls))

while (len(urls) > 0) and (len(targetUrls) < outNumUrl):
    try:
        curr_url = urls.pop(0)
        print("num. of URLs in stack: %d " %len(urls))
        print("Trying to access = " + curr_url)
        req = urllib.request.Request(curr_url, headers = {"User-Agent": "Mozilla/5.0"})
        webpage = urllib.request.urlopen(req).read() # urllib.request.urlopen(urllib.request.Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to acces = "+curr_url)
        print(ex)
        continue

    soup = BeautifulSoup(webpage)
    text = soup.get_text().lower()

    if ("covid" in text) and (curr_url not in targetUrls):
        targetUrls.append(curr_url)


    for tag in soup.find_all('a', href=True):
        childUrl = tag['href']
        o_childurl = childUrl
        childUrl = urllib.parse.urljoin(seed_url, childUrl)

        print("seed_url = " + seed_url)
        print("original childurl = " + o_childurl)
        print("childurl = " + childUrl)
        print("seed_url in childUrl = " + str(seed_url in childUrl))
        print("Have we seen this childUrl = " + str(childUrl in seen))

        if (hseed_url in childUrl) and (childUrl not in seen):
            print("***urls.append and seen.append***")
            seen.append(childUrl)
            urls.append(childUrl)
        else:
            print("######")

print("num. of URLs seen = %d, and scanned = %d" %(len(seen), len(opened)))

print("num. of webpages contain \'covid'\: %d" %len(targetUrls))

for i, url in enumerate(targetUrls):
    print(i, url, '\n')


