import re
from re import sub
from sys import stderr
from traceback import print_exc
import sys 
import requests

API_ENDPOINT = "https://doc.instantreality.org/tools/x3d_encoding_converter/convert/"
with open('simulacion.wrl', 'r') as file:
    wrl_data = file.read()

data = {'input_encoding': 'CLASSIC', 'output_encoding': 'HTML5', 'input_code': wrl_data}
r = requests.post(url=API_ENDPOINT, data=data)
output = re.search('<td class="code">(.+)</td></tr></table></pre>', r.text.replace('\n', ''))

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">") 
    s = s.replace("&#39;", "'")
    s = s.replace("&amp;", "&")
    return s

html_file = open("simulacion.html", "w")
pre_html = unescape(remove_html_tags(output.group(1)))
html_file.write(pre_html
    .replace("<body>", "<body bgcolor='000'>")
    .replace("400px", "1", 1)
    .replace("400px", "2", 1)
    .replace("0.7", "0.75")
    .replace("            <", '\n\t\t\t<')
    .replace("          <", '\n\t\t<')
    .replace("        <", '\n\t<')
    )
html_file.close()