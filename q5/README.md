# quantcast
[Platform Operations Interview Test for Quantcast](../../master/README.md)

## Question 5
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


## Answer
The tcpdump provided is an SSH session, between a client at `10.128.131.133` and a server listening at `10.122.0.110`. Since both endpoints are within 10/8, reserved in [RFC 1918](https://tools.ietf.org/html/rfc1918) as private address space, it can be assumed that these systems are not communicating directly over the public Internet. 


### Analysis
Following is a packet-by-packet breakdown of the exchange.

`10.128.131.133.59096 > 10.122.0.110.22: Flags [S], seq 2556384732, win 65535, length 0`
| Source      | 10.128.131.133.59096 |
| Destination | 10.122.0.110.22      |
| Flags       | SYN                  |
| Sequence    | 2556384732           |
| Ack range   | n/a                  |
| TCP window  | 65535                |
| Length      | 0                    |

Initial opening packet of the session, from the client 10.128.131.133 using source port 59096, to the server at 10.122.0.110 listening on port 22 (typically SSH). The client chooses an inital sequence number of 2556384732, and advertises a tcp receive window of 65535. This means the client is requesting an ack for every 64 kilobytes that it sends. Since the packet contains no data, because the tcp connection is "embryonic", the length of the tcp payload is 0 bytes.


`10.122.0.110.22 > 10.128.131.133.59096: Flags [S.], seq 3595295964, ack 2556384733, win 5840, length 0`
| Source      | 10.122.0.110.22      |
| Destination | 10.128.131.133.59096 |
| Flags       | SYN+ACK              |
| Sequence    | 3595295964           |
| Ack range   | Up to 2556384733     |
| TCP window  | 5840                 |
| Length      | 0                    |

This is the server's response to the client's SYN. It answers from local port 22, back to the client's randomly chosen ephemeral port number of 59096. The server chooses an inital sequence number of 3595295964, and acknowledges up to the next packet sent by the client. One of the earliest optimizations of tcp was to try to ack at most every second packet. The server advertises a tcp receive window of 5840 bytes.


`10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 1, win 65535, length 0`
| Source      | 10.128.131.133.59096 |
| Destination | 10.122.0.110.22      |
| Flags       | ACK                  |
| Sequence    | n/a                  |
| Ack range   | 1 Packet             |
| TCP window  | 65535                |
| Length      | 0                    |



`10.122.0.110.22 > 10.128.131.133.59096: Flags [P.], seq 1:21, ack 1, win 46, length 20`
| Source      | 10.122.0.110.22      |
| Destination | 10.128.131.133.59096 |
| Flags       | PSH+ACK              |
| Sequence    | 1 to 21              |
| Ack range   | 1 Packet             |
| TCP window  | 46                   |
| Length      | 21                   |



`10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 21, win 65535, length 0`
| Source      | 10.128.131.133.59096 |
| Destination | 10.122.0.110.22      |
| Flags       | ACK                  |
| Sequence    | n/a                  |
| Ack range   | Up to 21             |
| TCP window  | 65535                |
| Length      | 0                    |



`10.128.131.133.59096 > 10.122.0.110.22: Flags [P.], seq 1:22, ack 21, win 65535, length 21`
| Source      | 10.128.131.133.59096 |
| Destination | 10.122.0.110.22      |
| Flags       | PSH+ACK              |
| Sequence    | 1 to 22              |
| Ack range   | Up to 21             |
| TCP window  | 65535                |
| Length      | 21                   |



`10.122.0.110.22 > 10.128.131.133.59096: Flags [.], ack 22, win 46, length 0`
| Source      | 10.122.0.110.22      |
| Destination | 10.128.131.133.59096 |
| Flags       | ACK                  |
| Sequence    | n/a                  |
| Ack range   | Up to 22             |
| TCP window  | 46                   |
| Length      | 0                    |



`10.128.131.133.59096 > 10.122.0.110.22: Flags [P.], seq 22:814, ack 21, win 65535, length 792`
| Source      | 10.128.131.133.59096 |
| Destination | 10.122.0.110.22      |
| Flags       | PSH+ACK              |
| Sequence    | 22 to 814            |
| Ack range   | Up to 21             |
| TCP window  | 65535                |
| Length      | 792                  |



`10.122.0.110.22 > 10.128.131.133.59096: Flags [P.], seq 21:725, ack 22, win 46, length 704`
| Source      | 10.122.0.110.22      |
| Destination | 10.128.131.133.59096 |
| Flags       | PSH+ACK              |
| Sequence    | 21 to 725            |
| Ack range   | Up to 22             |
| TCP window  | 46                   |
| Length      | 704                  |



`10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 725, win 65535, length 0`
| Source      | 10.128.131.133.59096 |
| Destination | 10.122.0.110.22      |
| Flags       | ACK                  |
| Sequence    | n/a                  |
| Ack range   | Up to 725            |
| TCP window  | 65535                |
| Length      | 0                    |



