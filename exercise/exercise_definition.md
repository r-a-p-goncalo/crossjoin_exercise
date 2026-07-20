# Exercise description and tips

## Background

There is an application with a Microservices architecture.

2 instances of a service running spring boot, each receiving HTTP requests and communicating with a single Tuxedo service using Jolt.

As load increases, times of requests increase until the services are forced to restart. After, each pattern continues.

There are thread dumps of both services, which are to be studied.

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

Last Custom Call is more important, as it is the client's code

Make sure to think about queueing theory and System with high competing order requests

A microservice is just a small webserver, with a built-in tomcat and receiving requests