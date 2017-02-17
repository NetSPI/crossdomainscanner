# crossdomainscanner
Python tool to check for expired domains still allowed in crossdomain.xml files.

Released in preparation for an upcoming [NetSPI Blog](https://blog.netspi.com).
## Installation
```
~$ git clone https://github.com/NetSPI/crossdomainscanner
~$ cd crossdomainScanner
~$ pip install -r requirements.txt
[follow the example below for runtime usage]
```
## Example:

```
~$ python scanner.py https://jakereynolds.co -v -o output.txt
~$ cat output.txt
Searching crossdomain.xml on https://jakereynolds.co for unregistered domains

=============================================================

Crossdomain contents:
 - asdaasdasfwkjhcjhbwrgkljsv.com
 - thisisanexpireddomainaswell.es
 - thishasaninvalidTLD.invalidtld
  - Invalid TLD: invalidtld
 - jakereynoldsexpireddomain.com

Possible expired domains:
asdaasdasfwkjhcjhbwrgkljsv.com
thisisanexpireddomainaswell.es
jakereynoldsexpireddomain.com
```

This means that https://jakereynolds.co allows http://jakereynoldsexpireddomain.com in their crossdomain.xml file.  However, the latter is not registered to any DNS.  An attacker could now buy that domain and get full cross-domain access to https://jakereynolds.co

This tool is created for Ethical Hacking purposes, any illicit use is not related to its creator.
