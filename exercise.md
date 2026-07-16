
# Exercise description and tips

Microservices architecture

2 instances of a service running spring boot

Both receive HTTP requests

Both instances then call (jolt) the TUXEDO service, with a backend

Morning load is good, but as load increments, times of requests increase until service need to restart

After restart, the same pattern continues

Identify the root cause of the problem

Give suggestions

We have access to thread dumps

Generate a .csv file

Use an excel and pivot charts to resolve the problem

Make sure to use columns Last Custom Call and Last Call

Last Custom Call is more important, as it is the client's code

Make sure to think about queueing theory and System with high competing order requests

A microservice is just a small webserver, with a built-in tomcat and receiving requests

# Some technological Background

## Java

## SpringW

## Kubernetes

# Basic intepretation of data

## Thread dump names

For "tuxedo-adapter-service-primary-7b78c65dc8-nl95v_20210329015750":

- tuxedo-adapter-service-primary is the name of the service

- 7b78c65dc8 is kubernetes ReplicaSet hash

- nl95v is pod suffix

- 20210329017550 is time: year 2021, month 03, day 29, 01 hour, 75 mins, 50s

## General Thread Dump info

### nl95v

From the interpretation of the node nl95v, here:

<img src="data\interpreted\thread_count_by_timestamps_nl95v.svg" alt="nl95v.svg"/>

We can see that the thread count increases from 64 at 01:57:50 to 80 at 02:01:56 in slow pace. 

Right after, there is a quick increase from 135 at 02:02:57 until 164 at 02:15:22.

This mantains until 02:39:08. Right after, there is a slight increase to 169 threads. 

Then, a slight increase to 174 threads at 02:52:36.

Then, the number of threads reduce:
- 03:05:01 -> 85
- 03:06:02 -> 71
- 03:10:06 -> 49
- 03:11:07 -> 43
- 03:29:25 -> 41
- ends at 03:31:27 -> 41

The last row we have access too is at 03:31:27, with 41 threads

### sl494

From the interpretation of the node nl95v, here:

<img src="data\interpreted\thread_count_by_timestamps_sl494.svg" alt="sl494.svg"/>

The number of threads change as:
- start 01:51:35 -> 138
- 01:53:38 -> 69
- steadily increase until 02:01:48 -> 80
- 02:02:49 -> 128
- 02:05:55 -> 152
- steadily increases until 03:04:00 -> 173
- 03:05:02 -> 78
- 03:10:07 -> 45
- ends at 03:31:28 -> 41


### Both nodes

- sl494 starts first at 01:51:35, with the first two minutes having 138 threads
- At 01:53:38 both are online, having more or less 60 something threads
- Both increase and decrease conjointly, sharing behavior