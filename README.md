# E-Klase authentication example
- Written by Timur Bogdanov from Riga 51th Secondary School, 10B ❤️

Just something I was doing because I was bored during my programming classes...

I had an idea of creating a Telegram bot that fetches the diary from [e-klase.lv](https://e-klase.lv) and then sends useful things in the chat like what lessons will be today, what homework do we have and also what lesson will be next after the school bell. Even though I don't have that bot (yet!), I decided to share what I found while discovering e-klase's auth system.

It's actually much simpler than I thought.

The code example of logging in and getting the diary is in the repository - it's written in Python. You'll need to put your login and password in the `.env` file. Also, I won't mention this again, but for all requests you will need to have a usual `User-Agent` header (for example, the Firefox one).

## 1. POST request to main login page
First of all, we must send a POST request to this page: https://my.e-klase.lv/?v=15

The POST request must have the following data:
```json
{
    "UserName": "your_username",
    "Password": "your_password"
}
```
The official website also sends empty `fake_pass` and `cmdLogIn`, but you don't need them to get a diary. I honestly don't know what they're for.

The response will have 2 important things in its header - `.ASPXAUTH_EKLASE_3` cookie and the next redirect (`Location`). The cookie can already be used to check homepage, but it's dumb, because it will show you the homepage of the first school/class you went to. Moreover, I couldn't get it to work with the diary, but that's probably because e-klase deleted my diary from 8th class.

So instead, we will have to get a diffrent `.ASPXAUTH_EKLASE_3` cookie, by using the one we already have.

## 2. GET request to a redirect
The next redirect should be to this page: https://my.e-klase.lv/Family/PupilJoinOffer

We do a GET request to it with the cookies we got from the POST request to a login page. This one doesn't seem to do anything, but it gives us the next redirection link in the `Location` header.

## 3. Another GET request to a redirect
It should be this page: https://my.e-klase.lv/Family/UserLoginProfile/CheckForProfileSelection

We also do a GET request to it with the same login cookies, but this one's a little tricky. See, E-Klase has a strange auth system that requires 2 strange values - `TenantId` and `pf_id`. The `TenantId` one contains the id of the school/class(?) you're currently in. We can get them from this page.

In the code example of this repository, I use Python, so I can do this to get them:
```python
tenant_id_pattern = re.search(r"name='TenantId' value='(.*?)'", page_text)
pf_id_pattern = re.search(r"name='pf_id' value='(.*?)'", page_text)

tenant_id = tenant_id_pattern.group(1)
pf_id = pf_id_pattern.group(1)
```
And there you have it, you got those strange values. But we also need a redirect link, and it's not in the `Location` response header for some reason - instead, it's in the body text of this page. We can get it like so:
```python
redirect_url_pattern = re.search(r"^<form action='(.*?)'", text)
redirect_url = "https://my.e-klase.lv"+redirect_url_pattern.group(1)
```
Cool.

## 4. POST Request: The final redirect
This is the last redirect link: https://my.e-klase.lv/SessionContext/SwitchStudentWithFamilyStudentAutoAdd

You should do a POST request to it and get a better `.ASPXAUTH_EKLASE_3` cookie. I spent like half an hour trying to figure out why wasn't I getting it, until I realised that I was making a GET request instead of the POST one 😭

Anyway, in the POST request, you should send those 2 strange values from before, like so:
```json
{
    "TenantId": "IDACC-ORG-20080828-2398EF3B",
    "pf_id": "3000000"
}
```
Also don't forget to send the `.ASPXAUTH_EKLASE_3` cookie from the login request.

In the response, as I said before, you'll get an amazing `.ASPXAUTH_EKLASE_3` cookie. It's amazing, because with this one you can now access anything on the e-klase.

# 5. Get diary
Now we can get the HTML version of the diary. To do that, we make a GET request to this page: https://my.e-klase.lv/Family/Diary

Just don't forget to include our new `.ASPXAUTH_EKLASE_3` cookie.

As for parsing it and actually using it in a program - that's for a different time. If you have any questions, you may create an [issue](https://github.com/F1zzTao/EklaseAuth/issues) or contact me. All my contacts can be found on [my GitHub profile page](https://github.com/F1zzTao#user-content-contact-me-im-most-likely-bored-so-send-anything-please).

Thanks for reading!!
