


# Deeper evaluation of data

## General Thread Dump info

### nl95v

From the interpretation of the node nl95v, here:

<img src="..\data\interpreted\diagrams\thread_count_by_timestamps_nl95v.svg" alt="nl95v.svg"/>

We can see that the thread count increases from 64 at 01:57:50 to 80 at 02:01:56 in slow pace. 

Right after, there is a quick increase from 135 at 02:02:57 until 164 at 02:15:22.

This mantains until 02:39:08. Right after, there is a slight increase to 169 threads. 

Then, a slight increase to 174 threads at 02:52:36.

Then, the number of threads reduce:
- start 01:57:50 -> 64
- 02:01:56 -> 80, increasing at a slow pace
- 02:02:57 -> 135, increased rapidly
- 02:15:22 -> 164, increasing at a slow pace
- 02:39:08 -> 169, increased in a somewhat rapid pace
- 02:52:36 -> 174, increased at a somewhat rapid pace
- 03:05:01 -> 85
- 03:06:02 -> 71
- 03:10:06 -> 49
- 03:11:07 -> 43
- 03:29:25 -> 41
- ends at 03:31:27 -> 41

The last row we have access too is at 03:31:27, with 41 threads

### sl494

From the interpretation of the node sl494, here:

<img src="..\data\interpreted\diagrams\thread_count_by_timestamps_sl494.svg" alt="sl494.svg"/>

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


### Notes

sl494 starts first at 01:51:35, with the first two minutes having 138 threads

At 01:53:38 both are online, having more or less 60 something threads. This could mean they started sharing the load and so the pressure on sl493 was reduced. A counter argument to this is that the number of threads in sl494 actually reduces before the first timestamp for nl95v.

Both increase and decrease conjointly, sharing behavior

This may indicate that there is no problem specific to an instance of the service

The problem can either be connected to the rising number of threads, but that rise may also just be explained by more requests leading to more threads being available for them.

There is the possibility that the rise of threads is not, in any way, shape or form, correlated with the actual problem.

We also have to consider that these services may be working properly. Is there any visible problem beyond the number of threads?

## Evolution of status of threads

<img src="..\data\interpreted\diagrams\status_thread_count_by_timestamps_nl95v.svg" alt="nl95v.svg"/>

<img src="..\data\interpreted\diagrams\status_thread_count_by_timestamps_sl494.svg" alt="sl494.svg"/>

We can see that the number of threads in any status other than TIMED_WAITING mantains more or less constant, with the extra threads being almost all with TIMED_WAITING.


### Notes

Is the rise of the TIMED WAITING threads a problem?

A question to be made is why there are no more threads with RUNNABLE status, this means that as requests increase, the capability of concurrently processing requests does not increase, only the number of queued tasks?


## Evolution status of threads per category

### Tomcat

<img src="..\data\interpreted\diagrams\evol_of_state_for_tomcat.svg"/>

For tomcat exec:

<img src="..\data\interpreted\diagrams\evol_of_state_for_tomcat_exec.svg"/>

For tomcat exec without the TIMED WAITING threads:

<img src="..\data\interpreted\diagrams\evol_of_state_for_tomcat_exec_no_timed_waiting.svg"/>

We can see that most of the TIMED WAITING threads of tomcat and the system in a whole come from tomcat exec threads. These threads quickly increase to values above 100, making at every point in the lifetime of the services more than half of the threads running. A small percentage of them are running, and there are points where some are WAITING.

Are the WAITING threads a problem? Why are they WAITING? When we zoom in, we see that until 03:00, there are a few, 1-4 threads, either BLOCKED or RUNNABLE, which seems healthy. Beyound that point, the number of WAITING threads rises to 10. This is weird because it is after the peak of number of threads in the system, actually when they start reducing, and there are no exec threads in TIMED_WAITING state. Later we take notice that these are all executing `java.util.concurrent.LinkedBlockingQueue.take`.

Nevertheless, these are TIMED_WAITING threads. Are they waiting for something, and that wait is causing a bottleneck? Or are these threads simply waiting for a request, a task, that does not yet exist? Is it possible that too much of these idle threads were spawned prematurely, and they're stopping more relevant threads from being spawned?

### LLEN

<img src="..\data\interpreted\diagrams\evol_of_state_for_llen.svg"/>

<img src="..\data\interpreted\diagrams\evol_of_state_for_llen_only_blocked.svg"/>

We can see that the number of RUNNABLE and WAITING threads of LLEN are more or less always the same, peaking above 16. It is not a big percentage of the load, but the general form matches its pattern.

Later we understand that reading threads are the ones in the RUNNABLE state, and writing threads are WAITING.

### Notes

## Evolution of categories of threads of status

### Timed waiting threads

<img src="..\data\interpreted\diagrams\evol_of_cat_of_timed_waiting.svg"/>

We can see that most of the load comes from tomcat, peaking with more than 100 threads. It means that a big percentage of threads of any given moment are times waiting tomcat threads.

### Runnable threads


<img src="..\data\interpreted\diagrams\evol_of_cat_of_runnable.svg"/>

We can see that there is a pattern close to the load we're receiving, comming from LLEN. It peaks only at 18 threads, which is relatively small.

### Waiting threads

<img src="..\data\interpreted\diagrams\evol_of_cat_of_waiting.svg"/>

We can see that there is a pattern close to the load we're receiving, comming from LLEN. It peaks only at 17 threads, which is relatively small.

### Notes

Conjointly, the LLEN Runnable and Waiting threads increase to a peak of 35, mantaining more or less the same number.

## Last custom call of threads evolution

<img src="..\data\interpreted\diagrams\evol_of_last_custom_call.svg"/>

We can see that the increase, in the case of last custom calls, is on `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, which peaks at 80 and is more or leass always the highest number. Even so, it does not seem to follow any specific pattern, and so it is not worth that much attention. 

<img src="..\data\interpreted\diagrams\evol_of_last_custom_call_no_borrow.svg"/>

Looking without it, it is easy to notice that no specific pattern seems to be also followed by the other function calls. 

Interestingly, `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` is the second highest custom call present, peaking at 15. It is noticeble that it seems to increase with the load before peaking.

### Notes

Maybe `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` should follow the same pattern as the increase in load, but some bottleneck is not letting it? 

As we'll notice earlier, it seems like `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` is part of `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` execution. A question to be made is: Does the condition that usually stops `callServiceGeneric` from moving happens before or after the execution of `borrowSession`?


## Last call of threads evolution

<img src="..\data\interpreted\diagrams\evol_of_last_non_custom_call.svg"/>

We can see that most of the increase is on the `java.util.concurrent.LinkedBlockingQueue.poll`, spiking up to 113 threads doing it. This does not appear to totally follow the load increase pattern.

Secondly, we have `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`, spiking up to 78 threads. This appears to totally not follow the load increase pattern.

Without those two, we have:

<img src="..\data\interpreted\diagrams\evol_of_last_non_custom_call_no_poll_no_pollfirst.svg"/>

Where we can see, acompanying the server load, `java.net.SocketInputStream.socketRead`, spiking to a maximum of 19 threads doing the method.

Also accompanying the server load, we have `java.util.concurrent.LinkedBlockingQueue.take`, spiking to a maximum of 19 threads.

## Evolution of status of threads with call

### TuxedoTransaction.borrowSession


<img src="..\data\interpreted\diagrams\evol_of_status_for_call_borrowSession.svg"/>

All cases of `TuxedoTransaction.borrowSession` are from TOMCAT threads, brobably TOMCAT_execution threads.

Most cases of `TuxedoTransaction.borrowSession` have `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`, at a TIMED_WAITING state, except for some, in WAITING state, that have the last_call `java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt`.

### TuxedoTransaction.callServiceGeneric


<img src="..\data\interpreted\diagrams\evol_of_status_for_call_callServiceGeneric.svg"/>

All cases of `TuxedoTransaction.callServiceGeneric` are from TOMCAT threads, brobably TOMCAT_execution threads.

Most cases of `TuxedoTransaction.callServiceGeneric` have `bea.jolt.IOBuf.waitOnBuf`, at a TIMED_WAITING state. Some have it in a blocked state. What is it waiting for? Is it waiting for an internal condition of the system or an outside response?

There are also cases in WAITING state, that have the last_call `java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt`.

There are other last calls, all at a Runnable state, those are:
- `bea.jolt.NwHdlr.recv` (to notice that it calls `bea.jolt.IOBuf.waitOnBuf`)
- `ch.qos.logback.classic...`
- and more

These are probably irrelevant, finishing quick and being part of the normal execution of the method.


### LinkedBlockingQueue.poll

<img src="..\data\interpreted\diagrams\evol_of_status_for_call_linked_poll.svg"/>

The threads that seem to be relevant come from TOMCAT, all in a TIMED_WAITING state. These are most of the threads of the system. Later, it appears that these threads are simply waiting for http requests to be processed.

### LinkedBlockingDeque.pollFirst and TuxedoTransaction.borrowSession


<img src="..\data\interpreted\diagrams\evol_of_status_for_call_linked_pollfirst.svg"/>

All cases of `pollFirst` are from `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, and are from TOMCAT threads. `TuxedoTransaction.borrowSession` calls this method.

### LinkedBlockingQueue.take

<img src="..\data\interpreted\diagrams\evol_of_status_for_call_linked_take.svg"/>

Most of these threads come from TOMCAT.

### SocketRead

<img src="..\data\interpreted\diagrams\evol_of_status_for_call_socket_read.svg"/>

We can see that socketRead spends all of its time as RUNNABLE.

We can also see that the pattern that threads running socketRead of the category LLEN follows the same pattern as the load, peaking at in 16 in nl95v and 17 in sl494.

### getFromQ

<img src="..\data\interpreted\diagrams\evol_of_status_for_call_getFromQ.svg"/>

We can see that getFromQ spends almost all of its time as WAITING, sometimes BLOCKED. All of its threads are from LLEN.

### Notes

## Relevant thread lifetimes

### LLEN Reader thread

Choosing the thread with id 162 in nl95v:

<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_162_functions.svg"/>
<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_162_cpu.svg"/>

This thread spawns at 01:57 and seizes to exist at 03:09.

It only executes `java.net.SocketInputStream.socketRead`.

We can see that this specific LLENReader thread spends most of its life as RUNNABLE, executing socketRead0, and steadily increasing its cpu time from 60 ms to 1660 ms (1.7 seconds). Even so, this is small, having in account that the thread exissted for more than 10 minutes.

### LLEN writer thread

Choosing the thread with id 163 in nl95v:

<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_161_functions.svg"/>
<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_161_cpu.svg"/>

This thread spawns at 01:57 and seizes to exist at 03:09.

It only executes `bea.jolt.OutQ.getFromQ`.

We can see that this specific LLENReader thread spends most of its life as WAITING, executing socketRead0, and steadily increasing its cpu time from 60 ms to 1689 ms (1.7 seconds). Even so, this is small, having in account that the thread exissted for more than 1 hour and 10 minutes.

### Tomcat worker thread

Choosing the thread with id 183 in nl95v:

<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_183_functions.svg"/>
<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_183_cpu.svg"/>
<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_183_cpu_since_last.svg"/>

This thread spawns at 01:57 and seizes to exist at 03:03.

It spends most of its time executing `java.util.concurrent.LinkedBlockingQueue.poll` in a TIMED WAITING state. This is means waiting for a request to arrive so it can process it.

It also executes `bea.jolt.IOBuf.waitOnBuf` inside `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`, rarely blocked.

It also executes `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst` inside `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, always in TIME_WAITING.

The thread goes steadily from 3288 ms at 01:57 to 7141 ms cpu time. This means going from 3 seconds to 7 seconds in more than 1 hour and 6 minutes.

We'll also take a look into thread 185, as it doesn't ever enter the BLOCKED state.

<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_185_functions.svg"/>
<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_185_cpu.svg"/>
<img src="..\data\interpreted\diagrams\thread_lifetime_nl95v_185_cpu_since_last.svg"/>

It seems to share the same behavior, indicating that the BLOCKED state in these types of threads is not relevant.

## Threads that call a function

### callServiceGeneric

<img src="..\data\interpreted\diagrams\thread_that_call_callServiceGeneric.svg"/>
<img src="..\data\interpreted\diagrams\thread_that_call_callServiceGeneric_filtered_status.svg"/>

We can see that, in nl95v, 103 distinct threads call `callServiceGeneric` on `waitOnBfuf`, with 17 threads ever being with the BLOCKED status.

## Evolution of cpu since last per thread category

### Global view

#### Average cpu used in a minute

<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_all_cats_avg.svg"/>

We can see that the thread category that has the highest "cpu since last" is the category "Generic Thread Pool", peaking close to 2500 ms, or 2.5 seconds per minute.

If we remove generic, tomcat and jvm, we get:

<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_all_cats_avg_no_generic_no_tomcat.svg"/>

Where we can see the threads in the category of "jaeger" rise and peak at about 80 ms, or 0.08 s average per minute per thread. Bellow are "LLEN", which peak at about 15 ms, or 0.015 s per minute per thread

#### Total cpu used in a minute

<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_all_cats_total.svg"/>
<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_all_cats_total_no_generic.svg"/>

We can see that the category with the highest cummulative "cpu since last" is also the "Generic Thread Pool", peaking at about 13000 ms per minute, or 13s per minute. It is followed by TOMCAT, which peaks above 5000 ms, or 5s per minute. 

Also removing tomcat and jvm internal (which has only one weird peak in nl95v), we have:

<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_all_cats_total_no_generic_no_tomcat.svg"/>

Where we can see that LLEN follows the same pattern, peaking close to 400 ms, or 0.4s per minute.

We also see jaeger following the same pattern, peaking at 160 ms, or 0.2s per minute.

### TOMCAT

The sum is:
<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_tomcat_sum.svg"/>

We can see that the sum seizes to increase at the peak of the services.

The average is:
<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_tomcat_avg.svg"/>

We can see an increase at the begining of the service, and then the tomcat threads become stable, close to 50 of ms / minute.

### LLEN

The average is:
<img src="..\data\interpreted\diagrams\evol_of_cpu_since_last_tomcat_avg.svg"/>

We can see an increase at the begining of the service, peaking at 15 ms / minute, then reducing close to 10 ms / minute.

## Some more specific data

This space is for data that is got due to specific suspicious information

### The TOMCAT threads

The TIMED_WAITING threads are all executing `java.util.concurrent.LinkedBlockingQueue.poll`.

For an example of `java.util.concurrent.LinkedBlockingQueue.poll`, in nl95v, in timestamp 02:02:57:

	"http-nio-7012-exec-128" #302 daemon prio=5 os_prio=0 cpu=11.77ms elapsed=12.61s tid=0x00007f01340a3800 nid=0x10a5 waiting on condition  	[0x00007f00b49da000]
	   java.lang.Thread.State: TIMED_WAITING (parking)
		at java.util.concurrent.LinkedBlockingQueue.poll(java.base@11.0.10/LinkedBlockingQueue.java:458)
		at org.apache.tomcat.util.threads.TaskQueue.poll(TaskQueue.java:90)
		at org.apache.tomcat.util.threads.TaskQueue.poll(TaskQueue.java:33)
		at java.util.concurrent.ThreadPoolExecutor.getTask(java.base@11.0.10/ThreadPoolExecutor.java:1053)
		at java.util.concurrent.ThreadPoolExecutor.runWorker(java.base@11.0.10/ThreadPoolExecutor.java:1114)
		at java.util.concurrent.ThreadPoolExecutor$Worker.run(java.base@11.0.10/ThreadPoolExecutor.java:628)
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
		at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)

It seems like it is simply trying to get a task, an http request to process.

Regarding the WAITING threads,

<img src="..\data\interpreted\diagrams\tomcat_waiting_evol_of_state_and_funs.svg"/>

We can see that the increase of waiting threads is due to them executing `java.util.concurrentLinkedBlockingQueue.take`.

We can also see in an example stacktrace what it is doing:


	"http-nio-7012-exec-115" #289 daemon prio=5 os_prio=0 cpu=3007.57ms elapsed=4346.35s tid=0x00007f0134040000 nid=0x1098 waiting on condition  [0x00007f016e6c5000]
	   java.lang.Thread.State: WAITING (parking)
		at java.util.concurrent.LinkedBlockingQueue.take(java.base@11.0.10/LinkedBlockingQueue.java:433)
		at org.apache.tomcat.util.threads.TaskQueue.take(TaskQueue.java:108)
		at org.apache.tomcat.util.threads.TaskQueue.take(TaskQueue.java:33)
		at java.util.concurrent.ThreadPoolExecutor.getTask(java.base@11.0.10/ThreadPoolExecutor.java:1054)
		at java.util.concurrent.ThreadPoolExecutor.runWorker(java.base@11.0.10/ThreadPoolExecutor.java:1114)
		at java.util.concurrent.ThreadPoolExecutor$Worker.run(java.base@11.0.10/ThreadPoolExecutor.java:628)
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
		at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)

It seems like what happened was simply that requests stopped appearing, and so the tomcat threads started reducing in number, and those that remain simply use a method that gets the next task while waiting indefinetly, instead of using a timeout.


### LLEN threads

For the case of `java.net.SocketInputStream.socketRead0`, the one that is RUNNABLE, we have:

	"LLENwReader" #154 daemon prio=5 os_prio=0 cpu=766.65ms elapsed=4630.65s tid=0x00007f011c00c800 nid=0x5a5 runnable  [0x00007f00b79f8000]
	   java.lang.Thread.State: RUNNABLE
		at java.net.SocketInputStream.socketRead0(java.base@11.0.10/Native Method)
		at java.net.SocketInputStream.socketRead(java.base@11.0.10/SocketInputStream.java:115)
		at java.net.SocketInputStream.read(java.base@11.0.10/SocketInputStream.java:168)
		at java.net.SocketInputStream.read(java.base@11.0.10/SocketInputStream.java:140)
		at java.io.DataInputStream.readFully(java.base@11.0.10/DataInputStream.java:200)
		at bea.jolt.NwReader.run(NwHdlr.java:4001)

This is reading something from an internet socket, what?
It is called by, bea.jolt.NwReader.run, what is that?
Why does it seem like the number of threads running these are capped?

For the case of `bea.jolt.OutQ.getFromQ`, the one that is WAITING, we have:

	"LLENwWriter" #155 daemon prio=5 os_prio=0 cpu=671.72ms elapsed=4630.65s tid=0x00007f011c00f000 nid=0x5a6 in Object.wait()  [0x00007f00b78f7000]
	   java.lang.Thread.State: WAITING (on object monitor)
		at bea.jolt.OutQ.getFromQ(OutQ.java:89)
		- waiting to re-lock in wait() <0x00000000a258d730> (a bea.jolt.OutQ)
		at bea.jolt.NwWriter.run(NwHdlr.java:4366)

This is writing, what? Where is it getting the information?
Is it getting using `bea.jolt.OutQ.getFromQ` and then writting that information? From what queue does it get?

How are these two threads connected?
Are they responsible to communicate with the tuxedo backend?

If the threads are connected, and one is reading a message for the other to write in another point, it seems like the thread writting either is much faster (and so it is always WAITING), or there is a problem in the logic making it being unecessarely in the WAITING state.


### The TUXEDO execution of TOMCAT worker threads

For an example of com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric, in nl95v, in timestamp 02:02:57:

	"http-nio-7012-exec-139" #313 daemon prio=5 os_prio=0 cpu=12.75ms elapsed=11.63s tid=0x00007f01340b2800 nid=0x10b0 in Object.wait()  	[0x00007f00aece9000]
	   java.lang.Thread.State: TIMED_WAITING (on object monitor)
		at bea.jolt.IOBuf.waitOnBuf(IOBuf.java:119)
		- waiting to re-lock in wait() <0x00000000b82a85b8> (a bea.jolt.IOBuf)
		at bea.jolt.NwHdlr.recv(NwHdlr.java:1685)
		at bea.jolt.CMgr.recv(CMgr.java:235)
		at bea.jolt.JoltSession.recv(JoltSession.java:585)
		at bea.jolt.JoltRemoteService.call(JoltRemoteService.java:340)
		at bea.jolt.JoltRemoteService.call(JoltRemoteService.java:283)
		at com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric(TuxedoTransaction.java:136)
		at com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.sendPPGAMesage(TuxedoTransaction.java:72)
		at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController.ppgaService(TuxedoAdapterController.java:88)
		at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController$$FastClassBySpringCGLIB$$a341162e.invoke(<generated>)
		at org.springframework.cglib.proxy.MethodProxy.invoke(MethodProxy.java:218)
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.invokeJoinpoint(CglibAopProxy.java:771)
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163)
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:749)
		at org.springframework.validation.beanvalidation.MethodValidationInterceptor.invoke(MethodValidationInterceptor.java:123)
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:186)
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:749)
		at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:691)
		at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController$$EnhancerBySpringCGLIB$$c2540f2b.ppgaService(<generated>)
		at jdk.internal.reflect.GeneratedMethodAccessor117.invoke(Unknown Source)
		at jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(java.base@11.0.10/DelegatingMethodAccessorImpl.java:43)
		at java.lang.reflect.Method.invoke(java.base@11.0.10/Method.java:566)
		at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:197)
		at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:141)
		at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.	java:106)
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.	java:893)
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.	java:807)
		at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)
		at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1061)
		at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:961)
		at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006)
		at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:909)
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:652)
		at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:733)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at com.crossjointest.cbs.tuxedo.filter.ApplicationFilter.doFilter(ApplicationFilter.java:52)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.boot.actuate.metrics.web.servlet.WebMvcMetricsFilter.doFilterInternal(WebMvcMetricsFilter.java:93)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at io.opentracing.contrib.web.servlet.filter.TracingFilter.doFilter(TracingFilter.java:189)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:202)
		at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97)
		at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:542)
		at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:143)
		at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)
		at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78)
		at org.apache.catalina.valves.RemoteIpValve.invoke(RemoteIpValve.java:747)
		at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343)
		at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:374)
		at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65)
		at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:868)
		at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1590)
		at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
		- locked <0x00000000b39e0638> (a org.apache.tomcat.util.net.NioEndpoint$NioSocketWrapper)
		at java.util.concurrent.ThreadPoolExecutor.runWorker(java.base@11.0.10/ThreadPoolExecutor.java:1128)
		at java.util.concurrent.ThreadPoolExecutor$Worker.run(java.base@11.0.10/ThreadPoolExecutor.java:628)
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
		at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)

It seems like `bea.jolt.JoltRemoteService.call` calls the jolt remote service, and, later in its execution, it gets stuck at `bea.jolt.IOBuf.waitOnBuf`, in a condition of type `bea.jolt.IOBuf`. Seems like it is waiting for data to read. This can mean like this is an execution that already passed through `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, and is waiting for a response.

Another thing to note is that it locks a resource earlier, at `org.apache.tomcat.util.net.SocketProcessorBase.run`, of type `org.apache.tomcat.util.net.NioEndpoint$NioSocketWrapper`.

For an example of `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, in nl95v, in timestamp 02:08:07:

	"http-nio-7012-exec-16" #183 daemon prio=5 os_prio=0 cpu=4447.92ms elapsed=4517.88s tid=0x00007f013400d800 nid=0x6b2 waiting on condition  	[0x00007f016e5c3000]
	   java.lang.Thread.State: TIMED_WAITING (parking)
		at org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst(LinkedBlockingDeque.java:629)
		at org.apache.commons.pool2.impl.GenericObjectPool.borrowObject(GenericObjectPool.java:441)
		at org.apache.commons.pool2.impl.GenericObjectPool.borrowObject(GenericObjectPool.java:356)
		at com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession(TuxedoTransaction.java:197)
		at com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric(TuxedoTransaction.java:97)
		at com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.sendPPGAMesage(TuxedoTransaction.java:72)
		at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController.ppgaService(TuxedoAdapterController.java:88)
		at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController$$FastClassBySpringCGLIB$$a341162e.invoke(<generated>)
		at org.springframework.cglib.proxy.MethodProxy.invoke(MethodProxy.java:218)
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.invokeJoinpoint(CglibAopProxy.java:771)
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:163)
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:749)
		at org.springframework.validation.beanvalidation.MethodValidationInterceptor.invoke(MethodValidationInterceptor.java:123)
		at org.springframework.aop.framework.ReflectiveMethodInvocation.proceed(ReflectiveMethodInvocation.java:186)
		at org.springframework.aop.framework.CglibAopProxy$CglibMethodInvocation.proceed(CglibAopProxy.java:749)
		at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:691)
		at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController$$EnhancerBySpringCGLIB$$c2540f2b.ppgaService(<generated>)
		at jdk.internal.reflect.GeneratedMethodAccessor117.invoke(Unknown Source)
		at jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(java.base@11.0.10/DelegatingMethodAccessorImpl.java:43)
		at java.lang.reflect.Method.invoke(java.base@11.0.10/Method.java:566)
		at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:197)
		at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:141)
		at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.	java:106)
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.	java:893)
		at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.	java:807)
		at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)
		at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1061)
		at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:961)
		at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006)
		at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:909)
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:652)
		at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)
		at javax.servlet.http.HttpServlet.service(HttpServlet.java:733)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at com.crossjointest.cbs.tuxedo.filter.ApplicationFilter.doFilter(ApplicationFilter.java:52)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.boot.actuate.metrics.web.servlet.WebMvcMetricsFilter.doFilterInternal(WebMvcMetricsFilter.java:93)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)
		at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at io.opentracing.contrib.web.servlet.filter.TracingFilter.doFilter(TracingFilter.java:189)
		at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
		at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
		at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:202)
		at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97)
		at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:542)
		at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:143)
		at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)
		at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78)
		at org.apache.catalina.valves.RemoteIpValve.invoke(RemoteIpValve.java:747)
		at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343)
		at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:374)
		at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65)
		at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:868)
		at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1590)
		at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
		- locked <0x00000000b3b0dfa0> (a org.apache.tomcat.util.net.NioEndpoint$NioSocketWrapper)
		at java.util.concurrent.ThreadPoolExecutor.runWorker(java.base@11.0.10/ThreadPoolExecutor.java:1128)
		at java.util.concurrent.ThreadPoolExecutor$Worker.run(java.base@11.0.10/ThreadPoolExecutor.java:628)
		at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
		at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)


Something we can understand is that, if sessions are limited, this would become a bottleneck. In that case, `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` would have a variable number of threads running it, with the other executions of `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` being capped. This is veridied, indicating that this is the problem.

`org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst` is the last call.

The problem of contetion seems to exist here:

<img src="..\data\interpreted\diagrams\evol_of_status_funs_of_tomcat.svg"/>

While most TOMCAT threads are TIMED_WAITING are running `java.util.concurrent.LinkedBlockingQueue.poll`, there exists for example a spike in nl95v of TIMED_WAiting running `borrowSession` at 02:21, going up to 78. In the next minute, the execution is normal, but something to note is that `callServiceGeneric` never rises that high, looking like it is capped. This would create delays in users receiving responses.


### Contention zoom in

Zooming in close to the spike of `borrowSession` at 02:21 in nl95v,

<img src="..\data\interpreted\diagrams\evol_of_status_funs_of_tomcat_zoomed_21.svg"/>

In nl95v:

At 02:20, we have:
- `java.util.concurrent.LinkedBlockingQueue.poll` TIMED_WAITING: 82, threads waiting for an http request
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` TIMED_WAITING: 12, threads waiting for Tuxedo response
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` TIMED_WAITING : 9, threads waiting for session to process tuxedo request


At 02:21, we have:
- `java.util.concurrent.LinkedBlockingQueue.poll` TIMED_WAITING: 13, threads waiting for an http request
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` TIMED_WAITING: 12, threads waiting for Tuxedo response
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` TIMED_WAITING : 78, threads waiting for session to process tuxedo request

At 02:22, we have:
- `java.util.concurrent.LinkedBlockingQueue.poll` TIMED_WAITING: 84, threads waiting for an http request
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` TIMED_WAITING: 12, threads waiting for Tuxedo response
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` TIMED_WAITING : 7, threads waiting for session to process tuxedo request

One weird thing to note is that sl494 probably should jave show the same behavior, but it did not. Even so, that are other examples where both services have this kind of spike close to eachother, and both show this cap of `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` waiting.

Another possibility must be considered. Are TIMEOUTS happening?


### BLOCKED `callServiceGeneric` threads

Here we can see in nl95v wich threads ever reach "BLOCKED" status, which are 17 in nl95v and 11 in sl494. The number 17 is close to a lot of numbers that appear in this study, but has the number in sl949 is vastly different, it does not seem to mean anything. Beyond that, this state is rare for tomcat threads, appearing 2 times at most in the threads it appears. This means that the reason it may not appear in any other thread is because it is a state that is quickly solved. IT also appears at different times in every thread it appears, indicating that it probably is not correlated with anything.

<img src="..\data\interpreted\diagrams\thread_that_call_callServiceGeneric_filtered_status_blocked.svg"/>

One of those threads was one of the studied, with this tacktrace at 02:15:

	"http-nio-7012-exec-16" #183 daemon prio=5 os_prio=0 cpu=4864.98ms elapsed=5014.46s tid=0x00007f013400d800 nid=0x6b2 in 	Object.wait()  [0x00007f016e5c3000]
	   java.lang.Thread.State: BLOCKED (on object monitor)
		at bea.jolt.IOBuf.waitOnBuf(IOBuf.java:119)
		- waiting to re-lock in wait() <0x00000000b5716e58> (a bea.jolt.IOBuf)
		at bea.jolt.NwHdlr.send(NwHdlr.java:1571)
		at bea.jolt.NwHdlr.send(NwHdlr.java:1439)
		at bea.jolt.CMgr.send(CMgr.java:215)
		at bea.jolt.JoltSession.send(JoltSession.java:561)
		at bea.jolt.JoltRemoteService.call(JoltRemoteService.java:332)
		at bea.jolt.JoltRemoteService.call(JoltRemoteService.java:283)
		...