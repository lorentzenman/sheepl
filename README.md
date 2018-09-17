# sheepl
Sheepl : Creating realistic user behaviour for supporting tradecraft development within lab environments

## Introduction
There are lots of resources available online relating to how you can build AD network environments for the development of blue team and red team tradecraft. However the current solutions tend to lack one important aspect in representing real world network configurations. A network is not just a collection of static endpoints, it is a platform for communication between people.

Sheepl is a tool that aims to bridge the gap by emulating the behaviour that people normally undertake within a network environment. Using Python3 and AutoIT3 the output can be compiled into a standalone executable without any other dependancies that when executed on an Windows endpoint, executes a set of tasks randomly over a chosen time frame.

For red teamers this can serve to present those moments of opportunity to practice tradecraft.
For blue teamers this supports focusing on detection of malicious activity indicators inside a sequence of benign user tasks.


## Tooling
Sheepl has two modes, commandline and interactive where commandline can be used as part of a wider scripting solution and interactive allows you to build tasks in a question/response approach.

### Example

```
python3 sheepl.py --name TBone --total_time=2h --wordfile "c:\\users\\matt\\Desktop\\matt.doc" --inputtext "content/if.txt" --cmd --cc "ipconfig /all" --cc "whoami" --cc "netstat -anto -p tcp"')
```

The following video is an overview of Sheepl 0.1 as the beta release.

## YouTube Video

[![Alt text](https://img.youtube.com/vi/OQdulPd97y4/0.jpg)](https://www.youtube.com/watch?v=OQdulPd97y4)


## Acknowledgements
* The amazing AutoIT Language https://www.autoitscript.com
* Jonathan Bennett for creating ^^
* The amazing Python3 language https://www.python.org
* Fellow Spiders for tolerating me harping on about this stuff
