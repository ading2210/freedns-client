import freedns
import getpass
import os

#list subdomains in an account

username = input("username: ")
password = getpass.getpass(prompt="password: ")

print("logging in")
client = freedns.Client()
client.login(username, password)

subdomain = input("subdomain: ")
record_type = input("record type: ")
domain_id = input("domain id (14 for chickenkiller.com): ")
destination = input("destination: ")

print("requesting captcha")
captcha = client.get_captcha()
with open("/tmp/captcha.png", "wb") as f:
  f.write(captcha)
os.system("viu /tmp/captcha.png -h 18") #https://github.com/atanunq/viu
captcha_code = input("enter captcha: ")

client.create_subdomain(record_type, subdomain, domain_id, destination, captcha_code)
print("subdomain created")