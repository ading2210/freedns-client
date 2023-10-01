import freedns
import getpass
import os

#create a new account

client = freedns.Client()

email = input("email: ")
firstname = input("firstname: ")
lastname = input("lastname: ")
username = input("username: ")
password = getpass.getpass(prompt="password: ")

print("requesting captcha")
captcha = client.get_captcha()
with open("/tmp/captcha.png", "wb") as f:
  f.write(captcha)
os.system("viu /tmp/captcha.png -h 18") #https://github.com/atanunq/viu
captcha_code = input("enter captcha: ")

print("creating account")
client.create_account(captcha_code, firstname, lastname, username, password, email)
print("activation email sent")

activation_code = input("enter activation code: ")
client.activate_account(activation_code)
print("account creation finished")