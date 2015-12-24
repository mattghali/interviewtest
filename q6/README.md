# interviewtest
[Platform Operations Interview Test for MumbleCo](../../master/README.md)

## Question 6
A shared Linux system has become slow/unresponsive due to excesssive swapping. You (slowly) login as root and can issue a few commands. How would you identify and remediate the root cause of the problem? How would you ensure that it does not recur? List any commands used.


## Answer
A system in swap is a pain to troubleshoot since every command has to fight for its process space. Typically this is when `top` will fail to run. `ps aux` has a much better chance of finding memory and running in a reasonable time. Looking at the `%MEM` column should indicate if a single process is consumng excessive memory. Alternately a large number of smaller processes or threads in aggregate consuming excessive memory should also be obvious.

### Frequent causes
There are common cases for both single bloated processes and unusual numbers of smaller processes.

#### Memory leaks
Often long-running processes can develop memory leaks where chunks are allocated but never freed. Over time this can be observed as a near-linear decrease of free memory in monitoring graphs. The long-term solution for this case is identification of the offending code and a subsequent fix. Until that happens, workarounds include periodic process restarts, or setting a hard resource `ulimit` on memory for the process, assuming it is run as a service that is restarted if it dies.


#### Unusual quantity of workers/processes/threads
A daemon like Apache which services incoming requests with either many child processes or in-process threads can push a system into swap when the number of concurrently served requests increases. There are two general reasons this happens:
 * The rate of incoming requests suddenly increases. This can happen when one or more members of a load-balanced cluster become unavailable, when load balancing is misconfigured, or due to external events like a DDOS.
 * The average time taken for a request to complete increases while request rate remains constant. This can happen when the threads require an external dependency to complete, such as a storage IO operation, or database query.
Remediation of these cases depends on resolving the external events which triggered the unusual rate of requests, or the slow IO. Preventing them from happening is a matter of measuring the memory consumed per child/thread and dividing the amount of free memory by this size. This produces the maximum number of children/threads that the service should be allowed to spawn/fork. 


#### Plain misconfiguration
Misconfiguration of parameters like Apache's MPM settings can cause a system's memory usage to climb into swap. This can happen if normal traffic patterns are below what would cause the required number of threads or child processes to be run. As site traffic grows over time, eventually usage peaks will trigger a number of threads/processes that exceed the amount of memory available. Benchmarking, load testing, and configuration management can help prevent these events.

