import re
import http.client
import urllib.parse

conn = http.client.HTTPConnection('127.0.0.1', 8000)
conn.request('GET', '/signup/')
r = conn.getresponse()
body = r.read().decode('utf-8')
print('GET', r.status)
csrftoken = None
match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', body)
if match:
    csrftoken = match.group(1)
print('csrftoken', csrftoken)
cookies = r.getheader('Set-Cookie') or ''
print('cookies', cookies[:200])
params = urllib.parse.urlencode({
    'username': 'errorcheck',
    'email': 'error@x.com',
    'password1': 'complexpass123',
    'password2': 'complexpass123',
    'csrfmiddlewaretoken': csrftoken,
})
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': cookies,
    'Referer': 'http://127.0.0.1:8000/signup/',
}
conn.request('POST', '/signup/', params, headers)
r2 = conn.getresponse()
body2 = r2.read().decode('utf-8')
print('POST', r2.status)
print(body2[:2000])
