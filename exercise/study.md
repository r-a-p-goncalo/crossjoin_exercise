


# Deeper evaluation of data

## General Thread Dump info

### nl95v

From the interpretation of the node nl95v, here:

<img src="..\data\interpreted\thread_count_by_timestamps_nl95v.svg" alt="nl95v.svg"/>

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

<img src="..\data\interpreted\thread_count_by_timestamps_sl494.svg" alt="sl494.svg"/>

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

- At 01:53:38 both are online, having more or less 60 something threads. This could mean they started sharing the load and so the pressure on sl493 was reduced. A counter argument to this is that the number of threads in sl494 actually reduces before the first timestamp for nl95v.

- Both increase and decrease conjointly, sharing behavior

- This may indicate that there is no problem specific to an instance of the service

## Status of threads

### nl95v

From the interpretation of the node nl95v, here:

<img src="..\data\interpreted\status_thread_count_by_timestamps_nl95v.svg" alt="nl95v.svg"/>

We can see that the number of threads in any status other than TIMED_WAITING mantains more or less constant, with the extra threads being almost all with TIMED_WAITING.

### sl494


From the interpretation of the node sl494, here:

<img src="..\data\interpreted\status_thread_count_by_timestamps_sl494.svg" alt="sl494.svg"/>

We can see that the same holds true, noting that the extra overload the node has before the other is activated is also due to threads with the status TIMED_WAITING.

### Notes

We can see that, if there is an optimization to be made, it will be probably be showed by the threads with the status TIMED_WAITING.

A question to be made is why there are no more threads with RUNNABLE status, this means that as requests increase, the capability of concurrently processing requests does not increase, only the number of queued tasks?


## Evolution of threads per category



## Evolution of threads per status

### Timed waiting threads

From the interpretation of the number of time_waiting threads per thread category in the graph:

<img src="..\data\interpreted\status_time_waiting_thread_count_by_timestamps.svg" alt="sl494.svg"/>

We cam see that the extra number of threads all come from TOMCAT.

This could mean a focus in the study of the threads of that category:

* http-nio-7012...

  * BlockPoller
  * ClientPoller
  * Acceptor

* Catalina-utility-<?>

## Last custom call

From the interpretation of the number, for each unique value in custom_call, of threads that were with that call at snapshot time:

<img src="..\data\interpreted\thread_count_by_last_custom_call.svg" alt="sl494.svg"/>

We can see that the increase, in the case of last custom calls, is on `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`

A bit more irrelevant, but still present, is `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`

## Last call


From the interpretation of the number, for each unique value in last call, of threads that were with that call at snapshot time:

<img src="..\data\interpreted\thread_count_by_last_call.svg" alt="sl494.svg"/>

We can see that most of the increase is on the `java.util.concurrent.LinkedBlockingQueue.poll`, spiking up to 113 threads doing it. This does not appear to totally follow the load increase pattern.

Secondly, we have `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`, spiking up to 78 threads. This appears to totally not follow the load increase pattern.

Without those two, we have:

<img src="..\data\interpreted\thread_count_by_last_call_lesser.svg" alt="sl494.svg"/>

Where we can see, acompanying the server load, `java.net.SocketInputStream.socketRead`, spiking to a maximum of 19 threads doing the method.

Also accompanying the server load, we have `java.util.concurrent.LinkedBlockingQueue.take`, spiking to a maximum of 19 threads.

Taking a deeper look into those threads,

<img src="..\data\interpreted\status_of_linkedblockingqueue.take.svg" alt="sl494.svg"/>

We cam see that the increase is due to TOMCAT threads.

<img src="..\data\interpreted\status_of_socketRead.svg" alt="sl494.svg"/>

We can see that socketRead actually spends all of its time as RUNNABLE. A question to be made is, if this is related to processing requests, and it increases with the load, shouldn't it increase more? Peacking at 19 is weird when more than 140 threads. Another thing to note is that this happens in threads classified as "Redis"

## Look at tomcat threads and their purposes

The threads we currently have classified as "Tomcat" are:

- http-nio-7012...

  - BlockPoller

  - ClientPoller

  - Acceptor

  - exec-*

- Catalina-utility-<?>

`http-nio-7012-exec-*` threads are the most relevant. They are the threads whose number grows as the system becomes overloaded.

## Last call and Last custom call relations

From the thread relations between last calls and last custom calls, specially when filtered:

<img src="..\data\interpreted\last_calls_relations.svg" alt="sl494.svg"/>

<img src="..\data\interpreted\last_calls_relations_filtered.svg" alt="sl494.svg"/>

<img src="..\data\interpreted\last_calls_relations_filtered_custom_rows.svg" alt="sl494.svg"/>

We can see that `java.util.concurrent.LinkedBlockingQueue.poll` has 10388 cases, all of its appearances in our thread dumps, as not being associated with any last custom call.

We can see that `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`, in all of its 1278 cases, only appears with the last custom call `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`.

Also, `bea.jolt.IOBuf.waitOnBuf`, in all of its 1440 cases, only appears with the last custom call `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`

We can note that `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, which only has TIMED_WAITING and WAITING state:
- Has in all of its 1278 TIMED_WAITING states a Last call of `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`
-  Has in all of its 4 WAITING states a Last Call of `java.util.concurrent.locks.AbstractQueuedSynchronizer.parkAndCheckInterrupt`

We can note that `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`, which has BLOCKED, RUNNABLE, TIMED_WAITING, WAITING states:
- Has in all of its 1410 TIMED_WAITING states a Last Call of `bea.jolt.IOBuf.waitOnBuf`

## Look at threads with relevant last custom calls

We'll take a look into where com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession and com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric are called in the thread dumps, trying to undertand their purpose.

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

We can see:
- It is executed by a Tomcat worker thread
- the last custom call is for callServiceGeneric
- given its name, it is supposed to call the tuxedo external service
- the last call is bea.jolt.IOBuf.waitOnBuf
- there are two locks:
	- one of type org.apache.tomcat.util.net.NioEndpoint$NioSocketWrapper in function call org.apache.tomcat.util.net.SocketProcessorBase.run, which the thread has locked
	- another of type bea.jolt.IOBuf in function call bea.jolt.IOBuf.waitOnBuf, which the thread is waiting for

This thread appears to be handling an HTTP request that has already invoked the Tuxedo service and is currently blocked waiting for a response from the backend through Jolt. While waiting, it occupies a Tomcat request-processing thread.

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

We can see:
- It is executed by a Tomcat worker thread
- the last custom call is for borrowSession
- callServiceGeneric is present in the stacktrace, borrowSession is part of its execution
- given its name, it is borrowing a session to call the external service
- the last call is at org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst (which is one of the last calls of interest)
- there are two locks:
	- one of type org.apache.tomcat.util.net.NioEndpoint$NioSocketWrapper in function call org.apache.tomcat.util.net.SocketProcessorBase.run, which the thread has locked
	- another which is simply visible through the "waiting on condition"


This thread appears to be handling an incoming HTTP request that is attempting to obtain a Jolt session from the Commons Pool before invoking the Tuxedo service. The call to GenericObjectPool.borrowObject() is blocked while waiting for an available session, indicating that all pooled sessions are currently in use. Since the thread continues to occupy a Tomcat request-processing thread while waiting, increasing request latency or session pool exhaustion causes more request threads to accumulate, which matches the observed growth in http-nio-7012-exec-* threads over time.

## Look at threads with relevant last calls

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

We can see:
- It is executed by a Tomcat worker thread

For an example of `org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`, it is unecessary, as it only appears with the already studied `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` 

For an example of `java.util.concurrent.LinkedBlockingQueue.poll`, in nl95v, in timestamp 02:02:57:

	"LLENwReader" #154 daemon prio=5 os_prio=0 cpu=766.65ms elapsed=4630.65s tid=0x00007f011c00c800 nid=0x5a5 runnable  [0x00007f00b79f8000]
	   java.lang.Thread.State: RUNNABLE
		at java.net.SocketInputStream.socketRead0(java.base@11.0.10/Native Method)
		at java.net.SocketInputStream.socketRead(java.base@11.0.10/SocketInputStream.java:115)
		at java.net.SocketInputStream.read(java.base@11.0.10/SocketInputStream.java:168)
		at java.net.SocketInputStream.read(java.base@11.0.10/SocketInputStream.java:140)
		at java.io.DataInputStream.readFully(java.base@11.0.10/DataInputStream.java:200)
		at bea.jolt.NwReader.run(NwHdlr.java:4001)

	we also have

	"LLENwWriter" #155 daemon prio=5 os_prio=0 cpu=671.72ms elapsed=4630.65s tid=0x00007f011c00f000 nid=0x5a6 in Object.wait()  [0x00007f00b78f7000]
	   java.lang.Thread.State: WAITING (on object monitor)
		at bea.jolt.OutQ.getFromQ(OutQ.java:89)
		- waiting to re-lock in wait() <0x00000000a258d730> (a bea.jolt.OutQ)
		at bea.jolt.NwWriter.run(NwHdlr.java:4366)



## Look into interesting functions

Right now, given the numbers, the focus should be on `java.util.concurrent.LinkedBlockingQueue.poll` and where it is present. So, for that, we'll take a look into the last function on the stacktrace:
- `java.util.concurrent.LinkedBlockingQueue.poll`
- `org.apache.tomcat.util.threads.TaskQueue.poll`

the poll method of [LinkedBlockingQueue](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/LinkedBlockingQueue.html), which is an optionally-bounded blocking queue based on linked nodes, retrieves and removes the head of this queue, or returns null if this queue is empty.


the poll method of [TaskQueue](https://tomcat.apache.org/tomcat-10.0-doc/api/org/apache/tomcat/util/threads/TaskQueue.html), which is a task queue specifically designed to run with a thread pool executor, Retrieves and removes the head of this queue, or returns null if this queue is empty.

This shows what most threads are doing at the most critical moment: They are trying to get a task from the task queue. The reason they don't receive a task is simply because there isn't any.

Then there are two problems this could point to:
- Either threads that should be "abandoned" are not, or Tomcat should not produce so many threads in bursts to handle requests.
- Something is failing to produce the tasks to Tomcat.

There are two points in callServiceGeneric where we find TIMED_WAITING threads.

Given that a stacktrace where `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` appears, `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` also appears before it, we'll start by looking there:
- `at org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`
- `at org.apache.commons.pool2.impl.GenericObjectPool.borrowObject`
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`
- `com.crossjointest.cbs.tuxedo.controller.TuxedoAdapterController$$FastClassBySpringCGLIB$$a341162e.invoke`
- ...spring methods
- `org.apache.tomcat.util.net.SocketProcessorBase.run` (locks)

The pollFirst method of [LinkedBlockingDequeue](https://commons.apache.org/proper/commons-pool/xref/org/apache/commons/pool2/impl/LinkedBlockingDeque.html), which is an optionally-bounded BlockingDequeue based on linked nodes, removes the first element of the queue and returns it.

The borrowObject method of [GenericObjectPool](https://commons.apache.org/proper/commons-pool/apidocs/org/apache/commons/pool2/impl/GenericObjectPool.html), which is a configurable ObjectPool implementation, borrows an object from the pool using the specific waiting time which only applies if BaseGenericObjectPool.getBlockWhenExhausted() is true.

`com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession` seems to be borrowing a Jolt session from an Apache Commons Pool before the request can be sent to the Tuxedo backend. Since it ultimately calls `GenericObjectPool.borrowObject()`, the thread blocks whenever no session is immediately available.

`com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` is responsible for performing the actual remote call to the Tuxedo service.

The Spring methods  receive the HTTP request, dispatch it to the controller, and eventually return the generated response.

The Tomcat methods parse the HTTP request, assign the request to one of the `http-nio-7012-exec-*` worker threads, and keep that worker thread occupied until the complete response has been produced.


Now, when `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric` is stuck, it is on `bea.jolt.IOBuf.waitOnBuf`, so we should take attention to those methods.
- `bea.jolt.IOBuf.waitOnBuf`
- `bea.jolt.IOBuf` lock
- `bea.jolt.JoltRemoteService.call`
- `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`

[JoltRemoteService](https://docs.oracle.com/cd/E13203_01/tuxedo/tux80/javadoc/jolt/javadoc/bea/jolt/JoltRemoteService.html#JoltRemoteService(java.lang.String,%20bea.jolt.Session)) provides an implementation of the Tuxedo synchronous Request/Reply communication model. Jolt treats each Tuxedo service as a remote service, and each service has its input and output parameters. Typically, the user sets the input parameters through the various setXXX and addXXX methods, then invokes the call() method. Upon successful completion, the user retreives the results through the various getXXX methods.

`bea.jolt.IOBuf.waitOnBuf` could be waiting for the response, a more completed method so to say.

## Tomcat threads lifetime

Here we'll take attention to what are, for a thread name, the processes we see it taking.

<img src="..\data\interpreted\thread_timelife_nl95v_http-nio-7012-exec-100.svg" alt="sl494.svg"/>

Here we take a look into the thread http-nio-7012-exec-100 in node nl95v.

It is spawned at 02:02 and dies at 03:03.

It is hard to understand order of methods, as some information may be lost by thread dumps timings.

- `java.util.concurrent.LinkedBlockingQueue.poll`, waiting for a task to be available for it. This is the method were it spends the most time

- `at org.apache.commons.pool2.impl.LinkedBlockingDeque.pollFirst`, in `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.borrowSession`, in callGenericService.

- `bea.jolt.IOBuf.waitOnBuf` in `com.crossjointest.cbs.tuxedo.service.TuxedoTransaction.callServiceGeneric`.

An interesting thing is that it seems to rare to spend more than 1 minute in any method besides `java.util.concurrent.LinkedBlockingQueue.poll`.

This seems like healthy behavior.


<img src="..\data\interpreted\thread_timelife_nl95v_http-nio-7012-exec-102.svg" alt="sl494.svg"/>

Here we take a look into the thread http-nio-7012-exec-102 in node nl95v.

It is spawned at 02:02 and dies at 03:31.

In general, it follows the same pattern.

An interesting thing is that it spends all its time between 03:06 and 03:31 running `java.util.concurrentLinkedBlockingQueue.take` This seems to be after the server reset.


## Current understanding of the project

The application consists of two Spring Boot microservice instances exposing HTTP endpoints. Each incoming HTTP request is processed by a Tomcat worker thread (`http-nio-7012-exec-*`), routed through the Spring MVC pipeline to a controller, and eventually reaches `TuxedoTransaction.callServiceGeneric`.

Before contacting the backend, the service borrows a Jolt session from an Apache Commons Pool (`borrowSession`). Once a session is available, it performs a synchronous Jolt request to the Oracle Tuxedo service (`JoltRemoteService.call`). The Tomcat worker thread remains blocked until the Tuxedo service returns a response, after which the response propagates back through Spring and Tomcat to the HTTP client.

Overall, the request pipeline is:

```
HTTP Client
    ->
Tomcat (http-nio worker thread)
    ->
Spring MVC
    ->
Controller
    ->
TuxedoTransaction.borrowSession()
    ->
Apache Commons Pool (Jolt session)
    ->
TuxedoTransaction.callServiceGeneric()
    ->
Jolt
    ->
Oracle Tuxedo
    ->
Response
    ->
Spring MVC
    ->
Tomcat
    ->
HTTP Client
```

