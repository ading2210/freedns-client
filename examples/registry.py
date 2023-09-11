import freedns

#downloads and prints the domain registry

client = freedns.Client()
domains = client.get_registry()

for domain in domains:
  print(f'{domain["domain"]} | {domain["status"]}')