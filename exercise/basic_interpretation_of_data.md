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
  * exec

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