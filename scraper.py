#!/usr/bin/python
import re
import sys
import errno
import socket
import requests
import argparse
import subprocess
from socket import error as socket_error

#Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("domain", help="Search the crossdomain.xml file on <domain>, must be fully-qualified (i.e. http[s]://)")
parser.add_argument("-v", "--verbose", help="Print information to the console during runtime",action="store_true")
parser.add_argument("-o", "--output", type=str,
                    help="Write output to file")
args = parser.parse_args()


inputDomain = args.domain
verbose = args.verbose
if args.output:
    f = open(args.output, 'w')
    sys.stdout = f

if verbose:
    print("Searching crossdomain.xml on " + inputDomain + " for unregistered domains\n")
    print("=============================================================\n")

#Request the crossdomain file
crossDomain = requests.get(inputDomain+"/crossdomain.xml", timeout=10)
#Parse out all domains from the file
domains = re.findall(r'<allow-.*-from domain="(.*)"[ ]*?[\/]?>', crossDomain.text)
#Remove any duplicates
domains = list(set(domains))
possibleDomains = []
if verbose:
    print("Crossdomain contents: ")

for domain in domains:
    if verbose:
        print(" - " + domain)
    #Regex to get only the root domain or wildcard, am I missing any special characters?
    #Currently excludes subdomains
    domain = re.search(r'([a-zA-Z0-9-_~]+[.](?:[A-Za-z]{3,}|[A-Za-z]{2}\.[A-Za-z]{2}|[A-za-z]{2})(?:\n|$))|(^\*(?:\n|$))', domain)
    if domain is not None:
        domain = domain.group(0)
        #Is there a more elegant way to do this, than check in every loop?
        if domain == '*':
            print("\n------------Wildcard domain detected - YARD SALE------------")
            continue
	try:
            whoisOutput = output = subprocess.check_output(['whois', domain], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as errorThing:
            if errorThing.returncode == 1:
                possibleDomains.append(domain)

#Let the user know of any failed lookups
if len(possibleDomains) > 0:
    print("\nPossible expired domains: ")
    for domain in possibleDomains:
        print(domain)

#Do some cleanup
if args.output:
    sys.stdout = sys.__stdout__
    f.close()
