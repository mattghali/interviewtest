# quantcast
[Platform Operations Interview Test for Quantcast](../../master/README.md)

## Question 9
You have been tasked with archiving ten petabytes of raw log (ASCII text) data for an indefinite period of time. The data is currently broken up into 1 gigabyte files with unique filenames, and spread across 1000 commodity Linux systems. Discuss the potential solution(s) to this task, making sure to consider the following attributes of the solution: durability of the stored data, performance, implementation time, and cost.


## Answer
Assuming the question is addressing a single, 10pb snapshot of data (the current size of the entire Internet Archive) for simplicity, an apropriate solution would depend on the factors called out in the question. These factors are also very interdependent. The eventual purpose of the archive is also important to address.

The three primarily inter-related factors will be durability, performance, and cost. Generally, reliability * performance = cost, where a change of one factor directly affects one or more of the others.

#### Durability
Durability maps somewhat directly onto redundancy, which is a direct factor on cost. What is the value of the data? This can be calculated as the oportunity cost of losing it. Thus once availability factors are calculated, redundancy can be adjusted until the cost approximates the data's value.

#### Performance
The probability of the data's use in the future can be used as a first-order approximation of performance requirements. If it is being stored for an unlikely contingency such as an audit, probability will be lower; if it is being stored as a data warehouse probability will be closer to 1. Cost will be the product of the durability requirement and data use probability. However, as probability approaches 1, other factors become important like locality and access time. In this case, a better approximation would be the value extracted from the data (for instance by analytics) which should be comperable to the overall cost of the solution.


#### Cost
The overall cost of the archival solution is again, a factor of durability and performance. By controlling the redundancy of the information versus the performance, the cost should approximate the value which the data is expected to provide. However, cost is also affected by implementation time. The number of man-hours spent on the solution is a direct fraction of total cost.


### Summary
In summary, put it in s3. Netflix put a 10pb data warehouse in s3 and they are smart fellows. It will cost about $5 million a year, which, considering Amazon pays less per gb then we ever will, is a bargain. As a bonus it's available from ec2 whenever the data is actually required.


