# Exercise description and tips

## Background

There is an application with a Microservices architecture.

The reported problem is that the service, while dealing with the morning load, is stable. As this load increases, there starts to exist degradation in response times until a point where the service is restarted. When the service is restarted, performance is then acquired again, but, over times, the same pattern appears. It heals only when the load reduces again.

There were thread dumps taken, for the two services, accross a time interval, essentialy one per minute per service.


## Objective

Itentify the problem and, if possible, give suggestions on how to solve it.

## Deliverables

## Work pipeline

Create a parser for the thread dumps.

Save the data into a csv, which can then be imported into an excel.

The columns are: Timestamp, Thread Type, Thread name, Thread state, last call, last custom call

Through making pivot tables and charts, evaluate the results.

Identify the root cause of the problem

Give a suggestion on the solution

## Tips

Contention Analysis.

Last Custom Call is more important, as it is the client's code

Make sure to think about queueing theory and System with high competing order requests. How does the concurrency of the received requests work?

A microservice is just a small webserver, with a built-in tomcat and receiving requests