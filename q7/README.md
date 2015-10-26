# quantcast
[Platform Operations Interview Test for Quantcast](../../master/README.md)

## Question 7
You are asked to set up a network connection between two Linux system. One system will have the IP 10.0.10.5 while the other will have 10.0.11.6 – both with subnet mask of 255.255.255.0. What networking equipment will you use to perform this task? How will all system and network components be configured?


### Answer
The two systems are in different L2 networks; 10.0.10/24 and 10.0.11/24. They will require layer 3 routing to interconnect them, with a router interface on each /24.


#### Minimal
Requires: A router with two interfaces.

Configure one interface with an address on 10.0.10/24, and connect the corresponding linux system to this interface. Do the same for 10.0.11/24. Connections might require a crossover cable, depending on the age of the router ports and system NICs.

Configure static addressing on the linux systems using their distribution's config files- redhatish systems are in /etc/sysconfig/network-scripts, debianish are under /etc/network.


#### Upscale
Requires: A switch that does 802.1q trunking and layer 3 routing. Optional: dhcp server.

Enable routing. Define a VLAN interface on each of the two /24 networks. Configure a port for each system in 'access' mode on their respective vlan, and patch the systems into those ports.

Configure static addressing on the linux systems using their distribution's config files- redhatish systems are in /etc/sysconfig/network-scripts, debianish are under /etc/network. Or configure a dhcp server on the network to assign addresses to the systems. Remember to add a 'helper-address' on each vlan in the switch config, and to define networks in the dhcpd config for both /24s.


#### Router On  A Stick
Requires: A switch that does dot1q, a router, a dhcp server.

Configure an interface on the router with a dot1q interface for each /24. Patch into the switch. Configure that switchport as a dot1q trunk port, allowing both vlan ids. Configure a port on the switch for each linux system in access mode, on their respective vlans, and patch the systems into those ports.

Configure a dhcp server on the network to assign addresses to the systems. Remember to add a 'helper-address' on each vlan in the switch config, and to define networks in the dhcpd config for both /24s.

