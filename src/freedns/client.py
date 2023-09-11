import requests

BASE_URL = "https://freedns.afraid.org"

class Client:
  def __init__(self):
    self.headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    self.session = requests.Session() 
    self.session.headers.update(self.headers)

  def get_captcha(self):
    captcha_url = BASE_URL+"/securimage/securimage_show.php"
    response = self.session.get(captcha_url)
    return response.content
  
  def create_account(self, firstname, lastname, username, password, email, captcha_code):
    account_create_url = BASE_URL+"/signup/?step=2"
    payload = {
      "plan": "starter",
      "firstname": firstname,
      "lastname": lastname, 
      "username": username,
      "password": password,
      "password2": password,
      "email": email,
      "captcha_code": captcha_code,
      "tos": "1",
      "PROCID": "",
      "TRANSPRE": "",
      "action": "signup",
      "send": "Send+activation+email"
    }

    self.session.post(account_create_url, data=payload)
  
  def login(self, username, password): 
    login_url = BASE_URL+"/zc.php?step=2"
    payload = {
      "username": email,
      "password": password,
      "remember": "1",
      "submit": "Login",
      "remote": "",
      "from": "",
      "action": "auth"
    }

    self.session.post(login_url, data=payload)