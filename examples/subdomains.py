import freedns
import getpass

#list subdomains in an account

username = input("username: ")
password = getpass.getpass(prompt="password: ")

print("logging in")
client = freedns.Client()
client.login(username, password)

print("listing subdomains")
subdomains = client.get_subdomains()

for subdomain in subdomains:
  print(f'{subdomain["subdomain"]} | {subdomain["type"]} | {subdomain["destination"]}')
subdomain = subdomains[0]

print("getting details on "+subdomain["subdomain"])
subdomain = client.get_subdomain_details(subdomain["id"])
print(subdomain)