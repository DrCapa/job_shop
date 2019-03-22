# Job Shop

We consider a production process based on the 3 machines named A, B and C. Furthermore there are several job tickets with associated tasks. Every job is defined by the attributes task, machine and time. For example the job #1 is given by
|Task|Machine|Time|
|:---:|:---:|:---:|
| 1 | A | 3 |
| 2 | B | 2 |
| 3 | C | 2 |
The aim is to minimize the makespan of all jobs subject to several constraints like
* a machine can only work on one task at the same time,
* a task, once started, must run to completion,
* the order/sequence of the tasks have to be observed,
* no task for a associated job can be started until the previous task for that job is  completed.

The tool allows to define severla job in the given structure and gives back a gantt chart for the results.