# quantcast
Platform Operations Interview Test for Quantcast

## [Question 1](../master/q1)
Write a program or script (in any language) that performs the following task: Given a single file path as a command line argument, return the top ten most frequently-occurring IP addresses in the file. Assume the file contains only IP address delimited by a single line terminator. Optionally, allow for no restrictions on the contents of the input file.


## [Question 2](../master/q2)
Write a program or script (in any language) that performs the following task: Given a list of file paths as command line arguments, randomly choose a single line of text from the set of files and print it to stdout. Optionally, you may assume that all lines of text in all input files are of exactly the same length.


## [Question 3](../master/q3)
Write a program or script (in any language) that performs the following task: Given a list of hosts as command line arguments, print to stdout the combined size (in bytes) of all MySQL tables on all hosts. Assume each host runs the MySQL daemon (listening on the default port) and that you have MySQL admin privileges.


## [Question 4](../master/q4)
In as much detail as possible, explain what happens between the time a computer system is powered on and the operator is presented with a login prompt. Assume the hardware is a basic desktop system running Linux.


## [Question 5](../master/q5)
Describe in as much detail as possible the transaction(s) depicted below...
```
10.128.131.133.59096 > 10.122.0.110.22: Flags [S], seq 2556384732, win 65535, length 0
10.122.0.110.22 > 10.128.131.133.59096: Flags [S.], seq 3595295964, ack 2556384733, win 5840, length 0
10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 1, win 65535, length 0
10.122.0.110.22 > 10.128.131.133.59096: Flags [P.], seq 1:21, ack 1, win 46, length 20
10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 21, win 65535, length 0
10.128.131.133.59096 > 10.122.0.110.22: Flags [P.], seq 1:22, ack 21, win 65535, length 21
10.122.0.110.22 > 10.128.131.133.59096: Flags [.], ack 22, win 46, length 0
10.128.131.133.59096 > 10.122.0.110.22: Flags [P.], seq 22:814, ack 21, win 65535, length 792
10.122.0.110.22 > 10.128.131.133.59096: Flags [P.], seq 21:725, ack 22, win 46, length 704
10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 725, win 65535, length 0
```


## [Question 6](../master/q6)
A shared Linux system has become slow/unresponsive due to excesssive swapping. You (slowly) login as root and can issue a few commands. How would you identify and remediate the root cause of the problem? How would you ensure that it does not recur? List any commands used.


## [Question 7](../master/q7)
You are asked to set up a network connection between two Linux system. One system will have the IP 10.0.10.5 while the other will have 10.0.11.6 – both with subnet mask of 255.255.255.0. What networking equipment will you use to perform this task? How will all system and network components be configured?


## [Question 8](../master/q8)
A co-worker in San Francisco reports trouble accessing a company website in Japan. The site is hosted on a Linux system, and the user's Mac runs Mac OS X. Assuming you have unrestricted access (physical/logical) to company infrastructure, how would you debug this issue? List any commands you might use, and discuss other components of the system (besides the two computers) you might check.


## [Question 9](../master/q9)
You have been tasked with archiving ten petabytes of raw log (ASCII text) data for an indefinite period of time. The data is currently broken up into 1 gigabyte files with unique filenames, and spread across 1000 commodity Linux systems. Discuss the potential solution(s) to this task, making sure to consider the following attributes of the solution: durability of the stored data, performance, implementation time, and cost.



