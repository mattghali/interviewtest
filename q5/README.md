# interviewtest
[Platform Operations Interview Test for MumbleCo](../../master/README.md)

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

#### Packet 1
`10.128.131.133.59096 > 10.122.0.110.22: Flags [S], seq 2556384732, win 65535, length 0`

Field        | Data
------------ | ---------------------
Source       | 10.128.131.133.59096
Destination  | 10.122.0.110.22
Flags        | SYN
Sequence     | 2556384732
Ack range    | n/a
TCP window   | 65535
Length       | 0

Initial opening packet of the session, from the client 10.128.131.133 using source port 59096, to the server at 10.122.0.110 listening on port 22 (typically SSH). The client chooses an inital sequence number of 2556384732, and advertises a tcp receive window of 65535. This means the client is requesting an ack for every 64 kilobytes that it sends. Since the packet contains no data the length of the tcp payload is 0 bytes. At this point the client's "embryonic" connection is in the SYN_SENT state.


#### Packet 2
`10.122.0.110.22 > 10.128.131.133.59096: Flags [S.], seq 3595295964, ack 2556384733, win 5840, length 0`

Field        | Data
------------ | ---------------------
Source       | 10.122.0.110.22
Destination  | 10.128.131.133.59096
Flags        | SYN+ACK
Sequence     | 3595295964
Ack range    | Up to 2556384733
TCP window   | 5840
Length       | 0

This is the server's response to the client's SYN. It answers from local port 22, back to the client's randomly chosen ephemeral port number of 59096. The server chooses an inital sequence number of 3595295964, and acknowledges up to the next packet sent by the client. One of the earliest optimizations of tcp was to try to ack at most every second packet. The server advertises a tcp receive window of 5840 bytes. The server holds this connection in the SYN_RCVD state.


#### Packet 3
`10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 1, win 65535, length 0`

Field        | Data
------------ | ---------------------
Source       | 10.128.131.133.59096
Destination  | 10.122.0.110.22
Flags        | ACK
Sequence     | n/a
Ack range    | 1 Packet
TCP window   | 65535
Length       | 0

Final ACK from the client, taking this tcp connection to ESTABLISHED on both ends. At this stage, tcpdump has displayed the ISN from both sides of the connection, and now switches to relative sequence numbers, which are easier for humans to read and keep track of.


#### Packet 4
`10.122.0.110.22 > 10.128.131.133.59096: Flags [P.], seq 1:21, ack 1, win 46, length 20`

Field        | Data
------------ | ---------------------
Source       | 10.122.0.110.22
Destination  | 10.128.131.133.59096
Flags        | PSH+ACK
Sequence     | 1 to 21
Ack range    | 1 Packet
TCP window   | 46
Length       | 21

The server sends 21 bytes of traffic to the client. Now that the tcp session is established, the application protocol can begin. This is likely the ssh daemon sending its banner, using the PSH flag to signal tcp not to delay this packet. Otherwise tcp would try to collect many small packets into a larger packet closer to the receiver's window size. The server also sets its recieve window to a very small size, encouraging the client to immediately send data as well.


#### Packet 5
`10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 21, win 65535, length 0`

Field        | Data
------------ | ---------------------
Source       | 10.128.131.133.59096
Destination  | 10.122.0.110.22
Flags        | ACK
Sequence     | n/a
Ack range    | Up to 21
TCP window   | 65535
Length       | 0

The client acks the data received from the server, but has no additional data to send itself. At the application layer the ssh client may be waiting to complete keyboard authentication.


#### Packet 6
`10.128.131.133.59096 > 10.122.0.110.22: Flags [P.], seq 1:22, ack 21, win 65535, length 21`

Field        | Data
------------ | ---------------------
Source       | 10.128.131.133.59096
Destination  | 10.122.0.110.22
Flags        | PSH+ACK
Sequence     | 1 to 22
Ack range    | Up to 21
TCP window   | 65535
Length       | 21

The client sends over 21 bytes of data, also with the PSH flag set.


#### Packet 7
`10.122.0.110.22 > 10.128.131.133.59096: Flags [.], ack 22, win 46, length 0`

Field        | Data
------------ | ---------------------
Source       | 10.122.0.110.22
Destination  | 10.128.131.133.59096
Flags        | ACK
Sequence     | n/a
Ack range    | Up to 22
TCP window   | 46
Length       | 0

The server ACKs the 21 bytes sent by the client.


#### Packet 8
`10.128.131.133.59096 > 10.122.0.110.22: Flags [P.], seq 22:814, ack 21, win 65535, length 792`

Field        | Data
------------ | ---------------------
Source       | 10.128.131.133.59096
Destination  | 10.122.0.110.22
Flags        | PSH+ACK
Sequence     | 22 to 814
Ack range    | Up to 21
TCP window   | 65535
Length       | 792

Client sends 792 bytes of data to the server, with PSH set. At the same time, it again ACKs the 21 bytes it's received from the server.


#### Packet 9
`10.122.0.110.22 > 10.128.131.133.59096: Flags [P.], seq 21:725, ack 22, win 46, length 704`

Field        | Data
------------ | ---------------------
Source       | 10.122.0.110.22
Destination  | 10.128.131.133.59096
Flags        | PSH+ACK
Sequence     | 21 to 725
Ack range    | Up to 22
TCP window   | 46
Length       | 704

The server sends 704 bytes of data, with PSH set. It has not seen 22 through 814 from the client yet, either because of timing or loss, so it ACKs ip to 22.


#### Packet 10
`10.128.131.133.59096 > 10.122.0.110.22: Flags [.], ack 725, win 65535, length 0`

Field        | Data
------------ | ---------------------
Source       | 10.128.131.133.59096
Destination  | 10.122.0.110.22
Flags        | ACK
Sequence     | n/a
Ack range    | Up to 725
TCP window   | 65535
Length       | 0

The client ACKs data received from the server up to relative sequence number 725. This could mean it hasn't received 726 - 814 yet, or that the packets were dropped in transit.

The capture ends at this point.
