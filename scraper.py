#!/usr/bin/python
import os
import regex
import requests
from subprocess import Popen, PIPE, STDOUT
#TODO
#Add flags for verbose mode and input/output file



inputDomain = raw_input("Please enter fully-qualified domain name to search: ")
print("====================================================================================\n")
print("Searching crossdomain.xml on " + inputDomain + " for unregistered domains\n")
print("====================================================================================")
crossDomain = requests.get(inputDomain+"/crossdomain.xml", timeout=10)
domains = regex.findall(r'<allow-.*-from domain="(.*)"[ ]*?[\/]?>', crossDomain.text)
#remove any duplicates
domains = list(set(domains))
errorDomains = []
for domain in domains:
    #Regex to get only the root domain, am I missing any special characters?
    domain = regex.search(r'([a-zA-Z0-9-_~]+[.](?:[A-Za-z]{3,}|[A-Za-z]{2}\.[A-Za-z]{2}|[A-za-z]{2})(?:\n|$))', domain)
    if domain is not None:
        domain = domain.group(0)
        print(domain)
        try:
            sub = Popen("whois " + domain, shell=True, stdout=PIPE, stderr=PIPE)
            whoisOutput = sub.stdout.read()
            error_output = sub.stderr.read()
            if "fgets: Connection reset by peer" in error_output:
                errorDomains.append(domain)
            #Check for an error response from the whois command
            whoisError = regex.search(r'No match|NOT FOUND|Not fo|No Data Fou|has not been regi|No entri', whoisOutput)
            if whoisError is not None:
                print("Possible domain found: " + domain)
        except Exception as e:
            pass

#Let the user know of any failed lookups
if len(errorDomains) > 0:
    print("\nConnection reset by peer for the following domains: ")
    for domain in errorDomains:
        print(domain)