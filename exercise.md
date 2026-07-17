
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

In the thread dumps, it's worth noting that some of the threads present are from java itself, and are not counted in the number of threads presented at the begining of the dump

Regarding [thread states](https://docs.oracle.com/javase/8/docs/api/java/lang/Thread.State.html):
- NEW:  A thread that has not yeted started
- RUNNABLE: A thread executing in the java virtual machine
- BLOCKED: A thread that is blocked waiting for a monitor lock
- WAITING: A thread that is waiting indefinitly for another thread to perform
- TIMED_WAITING: A thread that is waiting for another thread to perform an action for up to a specified waiting time
- TERMINATED: A thread that has exited

## Spring

## Kubernetes

## TOMCAT / Apache

# Basic intepretation of data

This section is to note easily available information by simply doing a quick search on the files.

## Thread dump names

For "tuxedo-adapter-service-primary-7b78c65dc8-nl95v_20210329015750":

- tuxedo-adapter-service-primary is the name of the service

- 7b78c65dc8 is kubernetes ReplicaSet hash

- nl95v is pod suffix

- 20210329017550 is time: year 2021, month 03, day 29, 01 hour, 75 mins, 50s


We can notice that there are two pods, presumily representing each a different instance of the service:
- nl95v
- sl494

## Threads present

We can take attention to the names / prefixes of the thread names, and separating them into categories.

Name of thread category:
thread names

Name of thread category:
thread names

**JVM Internal Threads:**

* Reference Handler
* Finalizer
* Signal Dispatcher
* Service Thread
* C<?> CompilerThread0
* Sweeper thread
* Common-Cleaner
* DestroyJavaVM
* VM Thread
* VM Periodic Task Thread
* Attach Listener

**Garbage Collection (G1 GC):**

* GC Thread#0
* G1 Main Marker
* G1 Conc#0
* G1 Refine#0
* G1 Young RemSet Sampling

**Tomcat (HTTP Server):**

* http-nio-7012...

  * BlockPoller
  * ClientPoller
  * Acceptor

* Catalina-utility-<?>

**Spring Framework:**

* spring.cloud.inetutils

**Application Worker Threads:**

* container-<?>
* pool-2-thread-2
* AsynchThread-<?>

**Redis (Lettuce Client):**

* lettuce-eventExecutorLoop-1-1
* LLENw...

  * Reader
  * Writer

**Connection Pool Management:**

* commons-pool-evictor-thread

**AMQP / RabbitMQ:**

* AMQP Connection <?>

**Distributed Tracing (Jaeger):**

* jaeger.RemoteReporter...

  * QueueProcessor
  * FlushTimer

# Deeper evaluation of data

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

From the interpretation of the node sl494, here:

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
- At 01:53:38 both are online, having more or less 60 something threads. This could mean they started sharing the load and so the pressure on sl493 was reduced.
- Both increase and decrease conjointly, sharing behavior
- This may indicate that there is no problem specific to an instance of the service

## Status of threads

### nl95v

From the interpretation of the node nl95v, here:

<img src="data\interpreted\status_thread_count_by_timestamps_nl95v.svg" alt="nl95v.svg"/>

We can see that the number of threads in any status other than TIMED_WAITING mantains more or less constant, with the extra threads being almost all with TIMED_WAITING.

### sl494


From the interpretation of the node sl494, here:

<img src="data\interpreted\status_thread_count_by_timestamps_sl494.svg" alt="sl494.svg"/>

We can see that the same holds true, noting that the extra overload the node has before the other is activated is also due to threads with the status TIMED_WAITING.

### Conclusion

We can see that, if there is an optimization to be made, it will be probably be showed by the threads with the status TIMED_WAITING.

## Timed waiting threads

From the interpretation of the number of time_waiting threads per thread category in the graph:

<img src="data\interpreted\status_time_waiting_thread_count_by_timestamps.svg" alt="sl494.svg"/>

We cam see that the extra number of threads all come from TOMCAT.

This could mean a focus in the study of the threads of that category:

* http-nio-7012...

  * BlockPoller
  * ClientPoller
  * Acceptor

* Catalina-utility-<?>

## Last custom call

From the interpretation of the number, for each unique value in custom_call, of threads that were with that call at snapshot time:

<img src="data\interpreted\thread_count_by_last_custom_call.svg" alt="sl494.svg"/>

We can see that the increase, in the case of last custom calls, is on com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.burrowSession

A bit more irrelevant, but still present, is com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric 

## Last call


From the interpretation of the number, for each unique value in last call, of threads that were with that call at snapshot time:

<img src="data\interpreted\thread_count_by_last_call.svg" alt="sl494.svg"/>

We can see that most of the increase is on the java.util.concurrent.LinkedBlockingQueue.poll

Secondly, we have org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst


## Current state of study

These are the points to which we should take attention to:

- In the case of thread states:
    - TIMED_WAITING threads

- In the case of thread categories:
    - TOMCAT threads

- In the case of last calls:
    - java.util.concurrent.LinkedBlockingQueue.poll

    - org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst

- In the case of last custom calls:

    - com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.burrowSession

    -  com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric

Currently, what this appears is that:
- for each new request, a thread is spawned
- those threads spend most of their time simply waiting for a resource to be freed, meaning that is a locked shared resource that is sparse in relation to how much it is used