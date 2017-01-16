#!/usr/bin/python
import re
import sys
import errno
import whois
import socket
import argparse
import requests
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
validTLDs = [line.rstrip('\n') for line in open('TLD.txt')]
if args.output:
    f = open(args.output, 'w')
    sys.stdout = f

if verbose:
    print("Searching crossdomain.xml on " + inputDomain + " for unregistered domains\n")
    print("=============================================================\n")

#Request the crossdomain file
crossDomain = requests.get(inputDomain+"/crossdomain.xml", timeout=10)
#Parse out all domains from the file
domains = re.findall(r'<allow-.*-from domain="(.*?)"[ ]?.*[\/]?>', crossDomain.text)
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
    domainGroup = re.search(r'([a-zA-Z0-9-_~]+[.](?:[A-Za-z]{2}\.)?([A-Za-z]{2}|[A-za-z]{2}|[A-Za-z]{3,})(?:\n|$|\/))|(^\*(?:\n|$))', domain)
    if domainGroup is not None:
        domain = domainGroup.group(0)
        #Is there a more elegant way to do this, than check in every loop?
        if domain == '*':
            print("\n------------Wildcard domain detected - YARD SALE------------")
            continue
        #Make sure the TLD is valid
        #Does not check for valid SLD (ex: .co.uk, it only verifies .uk not .co)
        if domainGroup.group(2).lower() not in validTLDs:
            if verbose:
                print("  - Invalid TLD: " + domainGroup.group(2).lower())
            continue
    	try:
            #Run whois
            whoisOutput = whois.whois(domain)
            if whoisOutput.status is None:
                raise whois.parser.PywhoisError('error')
        except whois.parser.PywhoisError as errorOutput:
            try:
                #whois does not have full support (ex: .es domains), so double check false positives with socket
                whoisOutput = socket.gethostbyname(domain)
            except socket_error as serr:
                #[Errno 11001] getaddrinfo failed
                #[Errno 11004] getaddrinfo failed
                #Most likely cause is the domain name has not been purchased
                if serr.errno == 11001 or serr.errno == -2 or serr.errno == 11004:
                    possibleDomains.append(domain)


#Let the user know of any failed lookups
if len(possibleDomains) > 0:
    print("\nPossible expired domains: ")
    for domain in possibleDomains:
        print(domain)
else:
    print("No expired domains found")

#Do some cleanup
if args.output:
    sys.stdout = sys.__stdout__
    f.close()
