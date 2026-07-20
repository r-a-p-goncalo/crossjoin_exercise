## Current interpretation of the problem

### What is not the problem

- The application is not CPU-bound: most additional threads are in `TIMED_WAITING`, not `RUNNABLE`.
- There is no evidence of a JVM or garbage collection issue.
- The problem is not isolated to a single pod, since both instances exhibit the same behavior.
- Tomcat itself is not the root cause; its worker threads are blocked because they are waiting on downstream resources.

### What is the problem

The evidence indicates that request-processing threads spend most of their lifetime waiting instead of executing.

Two waiting points dominate:

- `borrowSession()`, where requests wait for an available Jolt session from the Commons Pool.
- `bea.jolt.IOBuf.waitOnBuf`, where requests wait for a response from the Tuxedo backend.

As backend latency increases or the pool of available Jolt sessions becomes exhausted, more Tomcat worker threads become blocked. Tomcat creates additional worker threads to continue serving incoming requests, causing the observed growth in `http-nio-7012-exec-*` threads. Eventually, a large portion of the thread pool is occupied by waiting requests, increasing latency for all clients and leading to service degradation.

### Solution suggestion

The bottleneck appears to be the synchronous communication with Tuxedo rather than the HTTP layer.

Possible improvements include:

- Verify whether the Jolt session pool is undersized and increase it if appropriate.
- Investigate why Tuxedo requests take so long to complete and optimize the backend service.
- Configure appropriate connection and request timeouts to avoid indefinitely occupied worker threads.
- Limit request concurrency or introduce back-pressure to prevent thread accumulation during overload.
- If feasible, replace the synchronous request model with an asynchronous architecture so that Tomcat worker threads are not blocked while waiting for backend responses.