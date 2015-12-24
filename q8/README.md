# interviewtest
[Platform Operations Interview Test for MumbleCo](../../master/README.md)

## Question 8
A co-worker in San Francisco reports trouble accessing a company website in Japan. The site is hosted on a Linux system, and the user's Mac runs Mac OS X. Assuming you have unrestricted access (physical/logical) to company infrastructure, how would you debug this issue? List any commands you might use, and discuss other components of the system (besides the two computers) you might check.


## Answer
I'll answer by addressing the general order I'd troubleshoot in, and the specific checks I'd run in each area to narrow down the set of possible problems. While a real-world troubleshooting session would follow a tree-shaped process, where the objective would be to quickly eliminate large branches of investigation, this isn't possible here. Instead I'll present troubleshooting with an order of operations designed to facilitate quickly eliminating areas of investigation as quickly as possible. 

Since this is a situation where a coworker is waiting, and some troubleshooting requires me to sit at his/her computer or remote desktop in, I will also try to frontload all tasks that would require me to interrupt work by being in exclusive control of the computer.


### General order of operations
At a high level, troubleshooting an issue like this is solved starting at the highest layer on the client side and working backwards. This results in a logical ordering to data collection, and also focuses on where the problem likely resides- in most "the website is down" cases, it is safe to assume that if there's only a single report of issues with a shared resource, the failure is most likely located on the client side; otherwise there would be many more reports of an outage, which the question doesn't mention.

Before jumping into a time-consuming analysis starting at the client, I'd make sure of a few obvious things that could be causing the problem:
 * Is the site in question down, for maintenance or other issues? If I can't contact the relevant admins, it is worth it to try from a few different points to narrow down where to start.
 * Does an adjacent computer load the site?
 * Does a computer on a different network load the site (try from a smartphone on its LTE network)


#### Client-side, application layer
More information is definitely needed to determine where to focus the investigation. Data I would collect either by asking the co-worker, or checking myself would include:
 * Is the computer able to load other pages on the same website?
 * Is the computer able to load other pages at different sites?
 * Using a browser's Developer timeline, what resource is failing to load? Is it blocking on the inital GET, or are most resources loading, and page rendering blocking on a single element?
 * Are there configuration issues on the client system interfering with the connection?


By checking on what resources the system is unable to load, I'll know where to look as I drill down futher in troubleshooting. If the system is unable to load other sites as well, it is most likely a connectivity issue, for example.  If the problem is restricted to a single site, then I'm able to verify that general IP connecivity isn't an issue. Connectivity issues could be caused by:
 * Browser configurations- proxy settings (in the application or system-wide)
 * Browser plugins/addons- there may be content filtering or ad-blocking software interfering. This can be verified by trying a different browser, and/or trying from a newly-created user account on the system.


#### Client-side, OS layer
Moving down the stack and armed with the app layer info, including results from the page load timeline, there could be OS level misconfigurations or issues.

 * Is the system having problems in general? A quick look at `top -o cpu` should show problems like excessive cpu load, or an unexpected amount of swap in use.
 * Am I able to resolve DNS for the website in question using `dig`; and do the results agree with `host`, which uses the system resolver libraries?
 * From the command line, am I able to connect to the required resources? HTTP resources can be checked by connecting `telnet` to port 80 of the webserver, HTTPS resources can be checked using `openssl s_client`.
 * Is the system able to open connections to other sites? Is there "personal firewall" or antivirus software interfering with new connections?


#### Client-side, network layer
Investgate connectivity from the client. Look at the system configuration and ensure there's no hard-coded settings overriding what should be set at boot time like DNS and routing. Ensure that resolv.conf agrees with the system preferences - while OSX applications don't depend on it, the os writes its current config to it; and some third-party tools which depend on libresolv may use it.

 * look at `netstat -an` and verify the correct default route.
 * Check for media errors/retransmits in `netstat -i`. If it shows errors, check on the aggregation switch that the client is on for logged errors for the switch port.
 * Check connectivity to dns resolvers using `ping` - is there any loss or unusual latency
 * Check connectivity to google.com with `ping` for any loss or latency
 * `ping` the website in question as well, it should likely show less latency than google
 * If there are any blocking resources from the pageload timeline, try pinging them as well
 * For any `ping` results showing loss/latency, try a `traceroute` to narrow down where the loss is occuring. Is it closer to the client or server?
 * Is the site public, or restricted to an internal company network? If restricted, is the client system on the correct network, and/or connected via VPN? Checking `ifconfig` and `netstat -rn` output will show what IP network it's on, and whether it's routing through a VPN tunnel.


#### Network layer
At this point I'd check to see if other users are reporting issues. Problems at this end of the connection will most likely be affecting a wider set of users. I'd then check network connecivity for the server, or cluster of servers, and any network gear in front of them.

 * Is there a firewall at the customer or server side of the network? If the client is on a wireless network, is there wireless network management? Either could possibly have 'quarantined' the client - check admin interfaces and logs if there are layer 3 connection failures.
 * Is there a load balancer in front of the cluster? Look at load balancing logs and admin interface to see if it is operating correctly. Is it showing a large number of backend timeouts or reporting 4xx or 5xx http errors?
 * Am I able to connect via http/https to the load balancer's VIP from the internet, or internal company network?
 * From the load balancer, am I able to ping its next routing hop?
 * From the load balancer, am I able to ping all of the backends?
 * If there are connectivity issues, look at the switches between the load balancer and its next-hop router(s). Are there ports down, bouncing, or reporting media errors? Are the ports showing sustained traffic levels close to their physical media max?
 * Look at the clusters' next-hop layer 3 router(s) logs. Has there been a hardware failure? Is there a pair of HSRP/VRRP routers failing back and forth, producing intermittent outages? Do the interfaces that connect the load balancer or server aggregation switch show media errors or link failures? (ios: `show int summary`, `sh int status err-disabled`, `show vrrp brief`, etc)
 * Do the routers have the correct routing configured? Has there been a link failure that has caused a route withdrawal? (ios: `sh ip route`, `sh ip bgp summary`, `sh ip ospf neighbor`, etc)


#### Server-side network layer
Verify layer 2 and layer 3 connecivity and configuration, similar to the network layer checks I'd run on the client side. Frequently in clustered architectures one member becomes misconfigured through operator error or config management errors; so quickly diff output of `netstat -rn` and `ifconfig -a` across cluster members and compare with the expected correct values. Ensure that autoconfigured parameters via dhcp/v6 router discovery are correct and haven't been hard-coded.

 * Can the servers ping their layer 3 next-hop router?
 * Does a `netstat -i` show any media errors or retransmits?
 * Are they correctly configured with loopbacks for DSR/etc on the load balancers?
 * Try `ping`/`traceroute` to the client address, hope it hasn't been blocked by overzealous security staff. Is the client reachable?


#### Server-side OS layer
Check logs, especially if there are layer 3 problems. Check the general OS health and storage availability. Ensure that the apropriate services are running. 
 * Look in `ipfw`/`iptables` for rules matching the client's address.
 * Check logs for software like `fail2ban`, make sure client hasn't been listed.
 * Check `top` and make sure cpu isn't saturated, excessive swap in use.
 * Ensure correct services (`apache`, `nginx` etc) are running via `ps`.
 * Do a quick `ls` in each mounted filesystem to make sure they're available.
 * Check `syslog` logfiles for OS/network problems. Look at `dmesg` for any kernel-level errors that are `printk()`'ed out instead of syslogged.


#### Server-side, app layer
Follow request flow from the network stack up. Requests are handled by an http/https server and most likely passed on via either a loadable module like mod_php, or passed to the next tier via a protocol like ajp. If the app has several tiers, iterate server-side network, OS and app layer checks up each tier.

 * Ensure web server is running via `ps` or `top`. Is the web server consuming the expected amount of CPU and memory? Compare across cluster members.
 * Check web/app server logfiles. Try running `tail -f` and watching for a request from the client if possible. Scan for any errors logged.
 * Diff web server configs across cluster members for any accidental config drift.
 * Check the web server's `server-status` or equivalent. Are the exepcted number of concurrent requests running? If there are a large number of threads blocking on IO, do they depend on external storage or a database operation?
 * Has there been a recent app code or configuration deployment? If so, is the app unavailable for all users? Consider a partial rollback of a single cluster member isolated from prod traffic to see if that resolves the issue.


#### Server-side, remote storage or database layer
Frequently problems at this layer manifest as a large number of errors/retries at the web server layer, or in less resilient architectures, a huge number of web server threads blocked on IO. This can lead to resource starvation at the OS layer, drawing attention to the symptom and not the cause, delaying resolution as admins try to "free up" memory by killing blocked threads/requests/queries. This can happen even if the storage or database is up and running requests/queries/iops, if the average operation latency pushes the number of concurrent threads at the web server layer past the number physical memory can support.

 * If storage/database is a managed service, check the relavent service status pages.
 * Check storage or database monitoring for changes in operation frequency. Often a new code deployment dramatically changes access patterns in unexpected ways. Inefficient storage access, or frequent queries to unindexed columns can quickly degrade performance.
 * Run a `show processlist` or equivalent on relational databases for clues of performance issues.
 * Refer to Cloudwatch statistics for services like RDS or DynamoDB to see if access patterns have dramatically changed, or if usage has remained constant but performance like query latency has changed. This could point to a service issue.
 * Check available metrics for changes in average request latency. This can also be caused by code changes, or growth of the 'hot' data set size beginning to push active data out of caching.
 * Look for changes in average age of data in any caching layer- inside the database or memcache, couchdb, Elastic Cache, etc. Also check whether utilization and hit rates have changed over time.
 * Compare database slow query logs for changes over time. This can be a direct cause (for example from a recent code change, abusive service access etc) or a symptom of a lower-level storage issue.
 * If storage is on some sort of hardware array, check the admin interface and any event logs. If there has been a hardware failure, storage could be slow/lossy during a failover or any sort of rebuild operation.


