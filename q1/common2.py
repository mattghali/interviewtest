#!/usr/bin/env python

'''
    This script accepts a text file as a command line argument, finds
    ip addresses in the text, then returns the 10 most common addresses
    in the text.
'''

import netaddr, sys

ipaddrs = dict()

# Read through file provided as command line argument
with open(sys.argv[1], 'r') as datafile:

    # break up input on word boundaries
    for word in datafile.read().split():

        # Filter out most uninteresting data
        if '.' in word:

            # Is word an ip address?
            try:
                addr = str(netaddr.IPAddress(word))

                if ipaddrs.has_key(addr):
                    # Increment existing refcount
                    ipaddrs[addr] += 1

                else:
                    # Add new addr to dictionary
                    ipaddrs[addr] = 1

            # word is not an ip address
            except netaddr.core.AddrFormatError:
                pass
            except ValueError:
                pass

results = []
# Now return the top 10 most frequent addresses
for addr in sorted(ipaddrs, key=ipaddrs.get, reverse=True):

    # append addr to list of results
    results.append(addr)

    # Break if we have our top 10 results
    if len(results) == 10: break

print results
