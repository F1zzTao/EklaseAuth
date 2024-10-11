import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

url_login = "https://my.e-klase.lv/?v=15"
url_diary = "https://my.e-klase.lv/Family/Diary"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
}
login_data = {
    'UserName': username,
    'Password': password,
}

"""
r = requests.get(url, headers=headers_login)
content = r.content
with open("eklas_diary.html", 'wb') as f:
    f.write(content)
"""

with requests.Session() as s:
    # Login
    print(f"First url: {url_login}")
    r_login = s.post(url_login, headers=headers, data=login_data, allow_redirects=False)
    redirect_url = "https://my.e-klase.lv"+r_login.headers['Location']
    print(f"Redirect url: {redirect_url}")

    # First redirect
    r_login_1 = s.get(redirect_url, headers=headers, cookies=r_login.cookies, allow_redirects=False)
    redirect_url = "https://my.e-klase.lv"+r_login_1.headers['Location']
    print(f"Next redirect url: {redirect_url}")

    # Second redirect
    r_login_2 = s.get(redirect_url, headers=headers, cookies=r_login.cookies, allow_redirects=False)

    # Getting TenantId and pf_id from second redirect
    content = r_login_2.content
    text = content.decode("utf-8")
    tenant_id_pattern = re.search(r"name='TenantId' value='(.*?)'", text)
    pf_id_pattern = re.search(r"name='pf_id' value='(.*?)'", text)

    tenant_id = tenant_id_pattern.group(1) if tenant_id_pattern else None
    pf_id = pf_id_pattern.group(1) if pf_id_pattern else None

    print(f"TenantId: {tenant_id}")
    print(f"pf_id: {pf_id}")

    login_datas = {
        "TenantId": tenant_id,
        "pf_id": pf_id
    }

    # Another redirect, through <form> now
    redirect_url_pattern = re.search(r"^<form action='(.*?)'", text)
    redirect_url = "https://my.e-klase.lv"+redirect_url_pattern.group(1)
    print(f"Next redirect url: {redirect_url}")
    r_login_2 = s.post(
        redirect_url,
        data=login_datas,
        headers=headers,
        cookies=r_login.cookies,
        allow_redirects=False
    )

    print("Getting diary...")
    r_diary = s.get(url_diary, headers=headers, cookies=r_login_2.cookies, allow_redirects=False)

with open("eklas_diary.html", 'wb') as f:
    f.write(r_diary.content)
