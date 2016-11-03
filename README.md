# crossdomainScanner
Python tool to check for expired domains still allowed in crossdomain.xml files

## Example:

```
python scraper.py
Please enter fully-qualified domain name to search: https://jakereynolds.co

Possible domain found: thishaskjwfkjansvkjwng.com
```

This means that https://jakereynolds.co allows http://thishaskjwfkjansvkjwng.com in their crossdomain.xml file.  However, the latter is not registered to any DNS.  An attacker could now buy that domain and get full cross-domain access to https://jakereynolds.co

This tool is created for Ethical Hacking purposes, any illicit use is not related to its creator.

Currently undergoing development
