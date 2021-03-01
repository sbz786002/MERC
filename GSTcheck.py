import http.client
import mimetypes
from codecs import encode

def check(gstno):
	conn = http.client.HTTPSConnection("app.mastergst.com")
	boundary = ''
	payload = ''
	headers = {
	  'authority': 'app.mastergst.com',
	  'method': 'GET',
	  'path': '/publicsearch1?gstin='+gstno+'&ipAddress=122.160.96.175&_=1609568705501',
	  'scheme': 'https',
	  'accept': ' */*',
	  'accept-encoding': ' gzip, deflate, br',
	  'accept-language': ' en-US,en;q=0.9',
	  'origin': ' https://mastergst.com',
	  'referer': ' https://mastergst.com/',
	  'sec-fetch-dest': ' empty',
	  'sec-fetch-mode': ' cors',
	  'sec-fetch-site': ' same-site',
	  'user-agent': ' Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
	  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
	}
	conn.request("GET", "/publicsearch1?gstin="+gstno+"&ipAddress=122.160.96.175&_=1609568705503", payload, headers)
	res = conn.getresponse()
	data = res.read()
	return data.decode("utf-8")