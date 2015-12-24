# interviewtest
[Platform Operations Interview Test for MumbleCo](../../master/README.md)

## Question 3
Write a program or script (in any language) that performs the following task: Given a list of hosts as command line arguments, print to stdout the combined size (in bytes) of all MySQL tables on all hosts. Assume each host runs the MySQL daemon (listening on the default port) and that you have MySQL admin privileges.


## Answers
From the question, it isn't clear whether the data required is the sum of table sizes on each host per host, or the sum across all hosts specified on the command line. I wrote the script `tablesize` to return both metrics. As the question instructed, I did not address any authentication for client connections.


A run of the following script is available via [travis-ci.org](https://travis-ci.org/mattghali/quantcast).


As a note, it may be advisable in production to calculate sizing using both data_length and index_length, replacing 'data_length' with 'sum(data_length, index_length)' on line 10. However the question specifically referred to table size, which is how I coded the answer.


```
[ec2-user@ip-10-0-2-17 ~]$ ./tablesize localhost localhost
localhost: 616145
localhost: 616145
total size: 1232290
```

