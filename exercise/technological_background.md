# Some technological Background

## Java

### Thread dumps

In the thread dumps, it's worth noting that some of the threads present are from java itself, and are not counted in the number of threads presented at the begining of the dump

A java thread dump will start with some header information:
- Timestamp
- Some information of the machine
- Thread id list and its length, without taking into account the internal java threads

Followed by, for each thread, some information regarding it and its stacktrace.

For example:


    "Reference Handler" #2 daemon prio=10 os_prio=0 cpu=38.35ms elapsed=28523.20s   tid=0x00007f01d032d800 nid=0xe waiting on condition  [0x00007f01b06fc000]
       java.lang.Thread.State: RUNNABLE
    	at java.lang.ref.Reference.waitForReferencePendingList(java.base@11.0.10/Native Method)
    	at java.lang.ref.Reference.processPendingReferences(java.base@11.0.10/Reference.java:241)
    	at java.lang.ref.Reference$ReferenceHandler.run(java.base@11.0.10/Reference.java:213)

or

    "Finalizer" #3 daemon prio=8 os_prio=0 cpu=111.91ms elapsed=28523.20s tid=0x00007f01d032f800    nid=0xf in Object.wait()  [0x00007f01b05fb000]
       java.lang.Thread.State: WAITING (on object monitor)
    	at java.lang.ref.ReferenceQueue.remove(java.base@11.0.10/ReferenceQueue.java:155)
    	- waiting to re-lock in wait() <0x00000000a030c170> (a java.lang.ref.ReferenceQueue$Lock)
    	at java.lang.ref.ReferenceQueue.remove(java.base@11.0.10/ReferenceQueue.java:176)
    	at java.lang.ref.Finalizer$FinalizerThread.run(java.base@11.0.10/Finalizer.java:170)

or

    "lettuce-eventExecutorLoop-1-1" #17 daemon prio=5 os_prio=0 cpu=13.53ms elapsed=28495.00s   tid=0x00007f01d189c800 nid=0x1a waiting on condition  [0x00007f016f0cb000]
       java.lang.Thread.State: TIMED_WAITING (parking)
    	at java.util.concurrent.LinkedBlockingQueue.poll(java.base@11.0.10/LinkedBlockingQueue.java:458)
    	at io.netty.util.concurrent.SingleThreadEventExecutor.takeTask(SingleThreadEventExecutor.java:256)
    	at io.netty.util.concurrent.DefaultEventExecutor.run(DefaultEventExecutor.java:64)
    	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:989)
    	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
    	at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
    	at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)

or 

    "http-nio-7012-ClientPoller" #94 daemon prio=5 os_prio=0 cpu=9248.76ms elapsed=28442.31s tid=0x00007f01d12d0800 nid=0x67 runnable   [0x00007f00b5ee9000]
       java.lang.Thread.State: RUNNABLE
    	at sun.nio.ch.EPoll.wait(java.base@11.0.10/Native Method)
    	at sun.nio.ch.EPollSelectorImpl.doSelect(java.base@11.0.10/EPollSelectorImpl.java:120)
    	at sun.nio.ch.SelectorImpl.lockAndDoSelect(java.base@11.0.10/SelectorImpl.java:124)
    	- locked <0x00000000a1e87cb8> (a sun.nio.ch.Util$2)
    	- locked <0x00000000a1e87610> (a sun.nio.ch.EPollSelectorImpl)
    	at sun.nio.ch.SelectorImpl.select(java.base@11.0.10/SelectorImpl.java:136)
    	at org.apache.tomcat.util.net.NioEndpoint$Poller.run(NioEndpoint.java:709)
    	at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)

or 

    "http-nio-7012-exec-158" #333 daemon prio=5 os_prio=0 cpu=959.09ms elapsed=1156.65s tid=0x00007f01340d2000 nid=0x10f5 in Object.wait()  [0x00007f00accc9000]
       java.lang.Thread.State: TIMED_WAITING (on object monitor)
    	at bea.jolt.IOBuf.waitOnBuf(IOBuf.java:119)
    	- waiting to re-lock in wait() <0x00000000baf50170> (a bea.jolt.IOBuf)
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
    	...
    	at org.springframework.aop.framework.CglibAopProxy$DynamicAdvisedInterceptor.intercept(CglibAopProxy.java:691)
    	at com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController$$EnhancerBySpringCGLIB$$c2540f2b.ppgaService(<generated>)
    	at jdk.internal.reflect.GeneratedMethodAccessor117.invoke(Unknown Source)
    	at jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(java.base@11.0.10/DelegatingMethodAccessorImpl.java:43)
    	at java.lang.reflect.Method.invoke(java.base@11.0.10/Method.java:566)
    	at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:197)
    	...
    	at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:909)
    	at javax.servlet.http.HttpServlet.service(HttpServlet.java:652)
    	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)
    	at javax.servlet.http.HttpServlet.service(HttpServlet.java:733)
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
    	...
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
    	at com.crossjointest.cbs.tuxedo.filter.ApplicationFilter.doFilter(ApplicationFilter.java:52)
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
    	...
    	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
    	...
    	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
    	at io.opentracing.contrib.web.servlet.filter.TracingFilter.doFilter(TracingFilter.java:189)
    	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
    	---
    	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:542)
    	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:143)
    	---
    	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343)
    	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:374)
    	---
    	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1590)
    	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
    	- locked <0x00000000b352b970> (a org.apache.tomcat.util.net.NioEndpoint$NioSocketWrapper)
    	at java.util.concurrent.ThreadPoolExecutor.runWorker(java.base@11.0.10/ThreadPoolExecutor.java:1128)
    	at java.util.concurrent.ThreadPoolExecutor$Worker.run(java.base@11.0.10/ThreadPoolExecutor.java:628)
    	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
    	at java.lang.Thread.run(java.base@11.0.10/Thread.java:834)


From which we can take out this information:
- Thread name
- Thread number
- Daemon flag
- Java priority
- OS priority
- cpu time in ms
- elapsed lifetime in s
- thread id
- native id
- native status
- thread state
- For each function call:
    - Function name
    - Function location
    - Locked reference and class if any, with maybe class

### Java multi threads

Regarding [thread states](https://docs.oracle.com/javase/8/docs/api/java/lang/Thread.State.html):
- NEW:  A thread that has not yeted started
- RUNNABLE: A thread executing in the java virtual machine
- BLOCKED: A thread that is blocked waiting for a monitor lock
- WAITING: A thread that is waiting indefinitly for another thread to perform
- TIMED_WAITING: A thread that is waiting for another thread to perform an action for up to a specified waiting time
- TERMINATED: A thread that has exited

## Spring

## Kubernetes

## [TOMCAT / Apache](https://en.wikipedia.org/wiki/Apache_Tomcat)

It provides an HTTP web server environment in which java code can also run.

Catalina is Tomcat's servlet container.


## [Tuxedo](https://en.wikipedia.org/wiki/Tuxedo_(software))

Tuxedo is a middleware platform used to manage distributed transaction processing in distributed computing environments. It is, at its core, a message routing and queuing system. Requests are sent to named services and tuxedo uses memory-based inter-process communication facilities to queue the requests to servers.



The heart of the tuxedo system is the bulleting board (BB). This is a shared memory segment that contains the configuration and state of a Tuxedo domain. Servers, services, transactions, and clients are all registered in the BB providing a global view of their state across the machines within a domain.

## [Jolt](https://docs.oracle.com/cd/E35855_01/tuxedo/docs12c/jdg/dvintro.html)

### [Oracle Jolt Components](https://docs.oracle.com/en/database/oracle/tuxedo/22/otxjo/oracle-jolt-components.html)

Jolt Servers and Repository Servers - one or more Jolt servers listen for network connections from clients, translate Jolt messages, multiplex multiple clients into a single process, and submit and retrieve requests to and from Oracle Tuxedo-based applications running on one or more Oracle Tuxedo servers.

Jolt class library - a Java package containing the class files that implement the Jolt API. These classes enable Java applications and applets to invoke Oracle Tuxedo services. The Jolt class library includes functionality to set, retrieve, manage, and invoke communication attributes, notifications, network connections, transactions, and services.

JoltBeans - Oracle JoltBeans provides a JavaBeans-compliant interface to Oracle Jolt. JoltBeans are Beans components that you can use in JavaBeans-enabled integrated development environments (IDEs) to construct Oracle Jolt clients. Jolt Beans consists of two sets of Java Beans: JoltBeans toolkit (a JavaBeans-compliant interface to Oracle Jolt that includes the JoltServiceBean, JoltSessionBean, and JoltUserEventBean) and Jolt GUI beans, which consist of Jolt-aware Abstract Window Toolkit (AWT) and Swing-based beans.

Jolt Internet Relay - the Jolt Internet Relay is a component that routes messages from a Jolt client to a Jolt Server Listener (JSL) or Jolt Server Handler (JSH). This component eliminates the need for the JSH and Oracle Tuxedo to run on the same machine as the Web server. The Jolt Internet Relay consists of the Jolt Relay (JRLY) and the Jolt Relay Adapter (JRAD).

Jolt ECID — The Jolt call process is as follows: JOLT client --> JSL/JSH --> tuxedo server --> service.

### [How Oracle Jolt Works]()

Using the following figure as an example, a simple banking application might have services such as INQUIRY, WITHDRAW, TRANSFER, and DEPOSIT. Typically, service requests are implemented in C or COBOL as a sequence of calls to a program library. Accessing a library from a native program means installing the library for the specific combination of CPU and operating system release on the client machine, a situation that Java was expressly designed to avoid. The Jolt Server implementation acts as a proxy for the Jolt client, invoking the Oracle Tuxedo service on behalf of the client. The Oracle Jolt Server accepts requests from the Jolt clients and maps those requests into Oracle Tuxedo service requests.

<img src="https://docs.oracle.com/en/database/oracle/tuxedo/22/otxjo/img/dvintro-1.1.1.jpg" alt="Oracle Jolt Architecture"/>

## Queueing theory

Arrivals are modeled with poisson distribution.

We can also model service ends (departures) with poisson distribution.

This can evolve into a model where the state is described by the current number of customers in the queue, and transitions with probability for transitioning for a state with one more customer, one less customer and equal number of customers.

The queue can be studied in relation to, tending to infinity, in which value it will stabilize in.