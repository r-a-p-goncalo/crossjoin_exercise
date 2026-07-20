# Current interpretation of the problem

## System description

The application consists of two Spring Boot microservice instances exposing HTTP endpoints. Each incoming HTTP request is processed by a Tomcat worker thread (`http-nio-7012-exec-*`), routed through the Spring MVC pipeline to a controller, and eventually reaches `TuxedoTransaction.callServiceGeneric`.

Before contacting the backend, the service borrows a Jolt session from an Apache Commons Pool (`borrowSession`). Once a session is available, it performs a Jolt request to the Oracle Tuxedo service (`JoltRemoteService.call`). The Tomcat worker thread remains blocked until the Tuxedo service returns a response, after which the response propagates back through Spring and Tomcat to the HTTP client.

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


## Reported symptoms and basic analysis

The reported problem is that the service, while dealing with the morning load, is stable. As this load increases, there starts to exist degradation in response times until a point where the service is restarted. When the service is restarted, performance is then acquired again, but, over times, the same pattern appears. It heals only when the load reduces again.

There were thread dumps taken, for the two services, accross a time interval, essentialy one per minute per service.

## Expected behavior

What is the behavior of the system if it was healthy?

What is the expected time for requests to be processed?

What would be its thread states in minute by minute thread dumps?

What would be its last calls and last custom calls in minute by minute thread dumps?

How would it behave if it was receiving more requests?

The expected behavior of an healthy system, regarding their threads states, last calls and custom calls, when receiving more requests, ... 

## What is not the problem

The problem is not isolated to a single pod, since both instances exhibit the same behavior.

Tomcat itself is not the root cause; its worker threads are blocked because they are waiting on downstream resources.

There is no evidence of a JVM or garbage collection issue.

There does not appear to exist a problem with internal processing, as cpu times look healthy, and there are not an increasing number of RUNNABLE threads.

## What is the problem

Wwhile most TOMCAT threads are TIMED_WAITING are running `java.util.concurrent.LinkedBlockingQueue.poll`, there exists for example a spike in nl95v of TIMED_WAiting running `borrowSession` at 02:21, going up to 78. In the next minute, the execution is normal, but something to note is that `callServiceGeneric` never rises that high, looking like it is capped. This would create delays in users receiving responses.

The problem simply seems to be a scarcity of jolt sessions, which create a bottleneck at `borrowSession`.

## Solution suggestion

If possible, these sessions should be increased. Another solution would be increasing the number of instances of the base service.
