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

  def detect_error(self, html):
    document = lxml.html.fromstring(html)

    table = document.cssselect('table[width="95%"]')[0]
    cell = table.cssselect('td[bgcolor="#eeeeee"]')[0]
    error_message = cell.text_content()
    return error_message.strip()

  def get_captcha(self):
    captcha_url = BASE_URL+"/securimage/securimage_show.php"
    response = self.session.get(captcha_url)
    return response.content
  
  def create_account(self, captcha_code, firstname, lastname, username, password, email):
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

    response = self.session.post(account_create_url, data=payload, allow_redirects=False)
    if response.status_code == 302:
      return

    #if we are not redirected, the signup has failed
    document = lxml.html.fromstring(response.text)
    signup_table = document.cssselect('table[width="420"]')[0]
    error_elements = signup_table.cssselect('b')

    error_messages = []
    for element in error_elements:
      error_messages.append("- "+element.text_content().strip())
    errors = "\n".join(error_messages)
    
    raise RuntimeError("Failed to initiate account creation. FreeDNS returned the following errors:\n"+errors)
  
  def activate_account(self, activation_code):
    activate_url = BASE_URL + f"/signup/activate.php?{activation_code}"

    response = self.session.get(activate_url, allow_redirects=False)
    if response.status_code != 302:
      error_message = self.detect_error(response.text)
      raise RuntimeError("Account activation failed. Error: "+error_message)

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

    response = self.session.post(login_url, data=payload, allow_redirects=False)
    if response.status_code != 302:
      error_message = self.detect_error(response.text)
      raise RuntimeError("Login failed. Error: "+error_message)
    
  def get_registry(self, page=1, sort=5, query=None):
    registry_url = BASE_URL+f"/domain/registry/?page={page}&sort={sort}"
    if not query is None:
      registry_url += f"&q={query}"

    html = self.session.get(registry_url).text
    document = lxml.html.fromstring(html)
    
    domains_str = document.cssselect('font[size="2"]')[0].text_content()
    domains_parsed = re.findall(r'Showing (\S+)-(\S+) of (\S+) total', domains_str)[0]
    domains_info = {
      "page_start": int(domains_parsed[0].replace(",", "")),
      "page_end": int(domains_parsed[1].replace(",", "")),
      "total": int(domains_parsed[2].replace(",", ""))
    }

    pages_str = document.cssselect('td[width="33%"][align="center"]')[0]
    current_page = pages_str.cssselect("input")[0].get("value")
    total_pages = pages_str.text_content().split()[-1]
    pages_info = {
      "current_page": int(current_page),
      "total_pages": int(total_pages)
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
      age_parsed = re.findall(r'(\d+) days{0,1} ago \((\S+)\)', age_text)[0]
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

    return {
      "domains_info": domains_info,
      "pages_info": pages_info,
      "domains": domains
    }
    
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
  
  def create_subdomain(self, captcha_code, record_type, subdomain, domain_id, destination):
    create_subdomain_url = BASE_URL+"/subdomain/save.php?step=2"
    payload = {
      "type": record_type,
      "subdomain": subdomain,
      "domain_id": domain_id,
      "address": destination,
      "ttlalias": "For+our+premium+supporters",
      "captcha_code": captcha_code,
      "ref": "",
      "send": "Save!"
    }
    
    response = self.session.post(create_subdomain_url, data=payload, allow_redirects=False)
    if response.status_code != 302:
      error_message = self.detect_error(response.text)
      raise RuntimeError("Failed to create subdomain. Error: "+error_message)
  
  def update_subdomain(self, subdomain_id, captcha_code, **kwargs):
    update_subdomain_url = BASE_URL+"/subdomain/save.php?step=2"

    defaults = self.get_subdomain_details(subdomain_id)
    get_arg = lambda x: kwargs.get(x) or defaults[x]
    payload = {
      "type": get_arg("type"),
      "subdomain": get_arg("subdomain"),
      "domain_id": get_arg("domain_id"),
      "address": get_arg("destination"),
      "ttlalias": "For our premium supporters",
      "captcha_code": captcha_code,
      "data_id": subdomain_id,
      "ref": "",
      "send": "Save!"
    }

    response = self.session.post(update_subdomain_url, data=payload, allow_redirects=False)
    if response.status_code != 302:
      error_message = self.detect_error(response.text)
      raise RuntimeError("Failed to update subdomain. Error: "+error_message)

  def get_subdomain_details(self, subdomain_id):
    subdomain_url = BASE_URL+f"/subdomain/edit.php?data_id={subdomain_id}"
    response = self.session.get(subdomain_url, allow_redirects=False)

    if response.status_code == 302:
      raise RuntimeError("Not authenticated.")
    document = lxml.html.fromstring(response.text)

    type_select = document.cssselect('select[name="type"]')[0]
    record_type = type_select.cssselect('option[selected]')[0].get("value")

    domain_select = document.cssselect('select[name="domain_id"]')[0]
    selected_domain = domain_select.cssselect('option[selected]')[0]
    domain = selected_domain.text_content().split(" ")[0]
    domain_id = int(selected_domain.get("value"))

    subdomain = document.cssselect('input[name="subdomain"]')[0].get("value")
    address = document.cssselect('input[name="address"]')[0].get("value")
    destination = document.cssselect('input[name="address"]')[0].get("value")
    wildcard = document.cssselect('input[name="address"]')[0].get("value") == "1"
    
    return {
      "type": record_type,
      "subdomain": subdomain,
      "domain": domain,
      "domain_id": domain_id,
      "destination": destination,
      "wildcard": wildcard
    }