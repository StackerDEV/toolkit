import requests, json, re

API_ENDPOINT_GITHUB = 'https://api.github.com/repos/'

""" 
for sourceforge use /rss suffix.
exmp https://sourceforge.net/projects/astrogrep/rss
format xml
"""

def getRelease(url): # github
    ret = dict()
    reg = re.compile("^[^\/]+:\/\/[^\/]*?\.?([^\/.]+)\.[^\/.]+(?::\d+)?\/")
    transformed_url = url.replace(reg.match(url).group(), API_ENDPOINT_GITHUB) + '/releases' # https://github.com/repos/{owner}/{repo}/releases/
    try:
		req = requests.get(url=transformed_url)
		req.raise_for_status()
		if req.status_code == 200:
			obj = json.loads(req.text)
			ret['browser_download_url'] = obj[0]['assets'][0]['browser_download_url'] #zipball_url = pjr src
			ret['tagname'] = obj[0]['assets'][0]['name']
			ret['published_at'] = obj[0]['published_at']
			releasename = obj[0]['assets'][0]['name']
			#newsuffix = ''.join((releasename.rsplit('.',1)[0], '.zip')) # why release in rar format ¯\_(ツ)_/¯ 
			ret['filename'] = releasename
			return ret
	except requests.exceptions.RequestException as e:
        raise SystemExit(e)
	
# benchmark results -> re takes more time -> but small amount of bandwidth is saved by using api.
