import requests
import re
import lxml.html

BASE_URL = "https://freedns.afraid.org"

class Client:
  def __init__(self):
    self.headers = {
      "Host": "freedns.afraid.org",
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate",
      "Connection": "keep-alive",
      "Upgrade-Insecure-Requests": "1",
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
      "username": username,
      "password": password,
      "remember": "1",
      "submit": "Login",
      "remote": "",
      "from": "",
      "action": "auth"
    }

    self.session.post(login_url, data=payload)
  
  def get_registry(self, page=1, sort=5):
    registry_url = BASE_URL+f"/domain/registry/?page={page}&sort={sort}"
    html = self.session.get(registry_url).text
    document = lxml.html.fromstring(html)
    
    domains_str = document.cssselect('font[size="2"]')[0].text_content()
    domains_parsed = re.findall(r'Showing (\S+)-(\S+) of (\S+) total', domains_str)[0]
    domains_info = {
      "page_start": int(domains_parsed[0].replace(",", "")),
      "page_end": int(domains_parsed[1].replace(",", "")),
      "total": int(domains_parsed[1].replace(",", ""))
    }

    pages_str = document.cssselect('td[width="33%"]')[-1].text_content()
    pages_parsed = re.findall(r'(\d+) of (\d+)', pages_str)[0]
    pages_info = {
      "current_page": int(pages_parsed[0]),
      "total_pages": int(pages_parsed[1])
    }

    table_rows = document.cssselect('tr.trl, tr.trd')
    domains = []
    for row in table_rows:
      cells = row.getchildren()

      domain_link = cells[0].getchildren()[0]
      domain = domain_link.text_content()
      domain_id = int(domain_link.get("href").split("=")[-1])

      hosts_span = cells[0].getchildren()[-1]
      hosts_count = int(re.findall(r'(\d+)', hosts_span.text_content())[0])

      status = cells[1].text_content()

      owner_link = cells[2].getchildren()[0]
      owner_name = owner_link.text_content()
      owner_id = int(re.findall(r'user_id=(\d+)&subject', owner_link.get("href"))[0])

      age_text = cells[3].text_content()
      age_parsed = re.findall(r'(\d+) days ago \((\S+)\)', age_text)[0]
      days_ago = int(age_parsed[0])
      date_created = age_parsed[1]

      domain_data = {
        "domain": domain,
        "id": domain_id,
        "hosts": hosts_count,
        "status": status,
        "owner_name": owner_name,
        "owner_id": owner_id,
        "age": days_ago,
        "created": date_created
      }
      domains.append(domain_data)

    return domains
    
  def get_subdomains(self):
    subdomains_url = BASE_URL+"/subdomain/"
    html = self.session.get(subdomains_url).text
    document = lxml.html.fromstring(html)

    form = document.cssselect('form[action="delete2.php"]')[0]
    tbody = form.getchildren()[0]

    subdomains = []
    for row in tbody.iterchildren():
      cells = row.getchildren()
      if len(cells) != 4: continue

      subdomain = cells[1].text_content()
      subdomain_link = cells[1].getchildren()[0]
      subdomain_id = subdomain_link.get("href").split("=")[-1]

      record_type = cells[2].text_content()
      record_value = cells[3].text_content()

      subdomain_data = {
        "subdomain": subdomain,
        "id": subdomain_id,
        "type": record_type,
        "destination": record_value
      }
      subdomains.append(subdomain_data)

    return subdomains