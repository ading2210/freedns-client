import freedns
import getpass
import os

#update a subdomain in your account

username = input("username: ")
password = getpass.getpass(prompt="password: ")

print("logging in")
client = freedns.Client()
client.login(username, password)

print("listing subdomains")
subdomains = client.get_subdomains()

for subdomain in subdomains:
  print(f'{subdomain["subdomain"]} | {subdomain["type"]} | {subdomain["destination"]}')
subdomain = subdomains[int(input("subdomain to edit: "))-1]

print("requesting captcha")
captcha = client.get_captcha()
with open("/tmp/captcha.png", "wb") as f:
  f.write(captcha)
os.system("viu /tmp/captcha.png -h 18") #https://github.com/atanunq/viu
captcha_code = input("enter captcha: ")
destination = input("destination: ")

client.update_subdomain(subdomain["id"], captcha_code, destination=destination)
print("subdomain updated")