# sheepl
Sheepl : Creating realistic user behaviour for supporting tradecraft development within lab environments

## Introduction
There are lots of resources available online relating to how you can build AD network environments for the development of blue team and red team tradecraft. However the current solutions tend to lack one important aspect in representing real world network configurations. A network is not just a collection of static endpoints, it is a platform for communication between people.

Sheepl is a tool that aims to bridge the gap by emulating the behaviour that people normally undertake within a network environment. Using Python3 and AutoIT3 the output can be compiled into a standalone executable without any other dependancies that when executed on an Windows endpoint, executes a set of tasks randomly over a chosen time frame.

For red teamers this can serve to present those moments of opportunity to practice tradecraft.
For blue teamers this supports focusing on detection of malicious activity indicators inside a sequence of benign user tasks.

## Sheepl 2.0 Updates

* Dynamic task importing and reloading
* New command line interface
* Encapsulated class based functionality
* JSON format profiles to support scripting pipeline
* Built in task template for boiler plate code
* Support for subtasking for specific modules i.e. RemoteDesktop
* Additional logic checks for discarding tasks, previous output and task completion

## Tooling
Sheepl has two modes, profile imports and interactive where commandline can be used as part of a wider scripting solution and interactive allows you to build tasks in a question/response approach.

### Example

```
python3 sheepl.py --interactive
```

### JSON Profiles

It is now possible to build and import sequences of Sheepl commands via JSON profiles

```
python3 sheepl.py --profile profiles/red.json
```

### Templates

You can now specify a boiler plate template file. This is achieved by using the following:

```
python3 sheepl.py --template NewTask --category network
```
This command will create the file within 'tasks/network' called 'NewTask' following the preferred camel case class names


### New Interactive Console

The console now has additional options for specifying Sheepl specific behaviours such as updating the task list, specifing looping options or whether the icon appears in the systen tray


```
Documented commands (type help <topic>):
========================================
create  finished  help  icon  list  loop  quit  task  update
```

## AutoIT3

You can download the AutoIT3 runtime and the Aut2EXE compiler here:
[AutoIT3 Download](https://www.autoitscript.com/site/autoit/downloads/)

The following video is quick demo of Sheepl 2.0 as the current release.

## YouTube Video

[![Alt text](https://img.youtube.com/vi/S4Zvw-IG1Pc/0.jpg)](https://www.youtube.com/watch?v=S4Zvw-IG1Pc)


## 44Con Workshop Video

(https://www.youtube.com/watch?v=ZErvmrP4UCg)


## Acknowledgements
* The amazing AutoIT Language https://www.autoitscript.com
* Jonathan Bennett for creating ^^
* The amazing Python3 language https://www.python.org
* Guido for creating ^^
