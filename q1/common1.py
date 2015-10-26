#!/usr/bin/env python

'''
    This script accepts a list of ip addresses as a command line argument,
    and returns the 10 most common addresses in the list.
'''

import sys

ipaddrs = dict()

# Read through list provided as command line argument
with open(sys.argv[1], 'r') as iplist:

    # Generate a dictionary of addresses and their frequency
    for addr in iplist.readlines():

        # Trim trailing newline
        addr = addr[:-1]

        if ipaddrs.has_key(addr):
            # Increment existing refcount
            ipaddrs[addr] += 1

        else:
            # Add new addr to dictionary
            ipaddrs[addr] = 1

results = list()

# Now return the top 10 most frequent addresses
for addr in sorted(ipaddrs, key=ipaddrs.get, reverse=True):

    # append addr to list of results
    results.append(addr)

    # Break if we have our top 10 results
    if len(results) == 10: break

print results
