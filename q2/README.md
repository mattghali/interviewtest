# quantcast
[Platform Operations Interview Test for Quantcast](../../master/README.md)

## Question 2
Write a program or script (in any language) that performs the following task: Given a list of file paths as command line arguments, randomly choose a single line of text from the set of files and print it to stdout. Optionally, you may assume that all lines of text in all input files are of exactly the same length.


## Answers
I couldn't tell from the question whether the objective was a single random line from each file, or a single random line from the set of files. So I coded a script to produce either result.


A run of the following scripts is available via [travis-ci.org](https://travis-ci.org/mattghali/quantcast).


### Scenario 1
The script `randomline.py` will return a randomly selected line from each filename given as a command line argument.

```
mghali@ernie.int.snark.net:~/work/quantcast/q2$ ./randomline.py /etc/passwd /etc/hosts
_cvs:*:72:72:CVS Server:/var/empty:/usr/bin/false

::1             localhost
```


### Scenario 2
The script `randomfile.py` will return a randomly selected line from a randomly selected file, out of the set given as a command line argument.

```
mghali@ernie.int.snark.net:~/work/quantcast/q2$ ./randomfile.py /etc/passwd /etc/hosts
# localhost is used to configure the loopback interface
```

