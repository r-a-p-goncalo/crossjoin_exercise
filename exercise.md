
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

## Spring

## Kubernetes

# Basic intepretation of data

## Thread dump names

For "tuxedo-adapter-service-primary-7b78c65dc8-nl95v_20210329015750":

- tuxedo-adapter-service-primary is the name of the service

- 7b78c65dc8 is kubernetes ReplicaSet hash

- nl95v is pod suffix

- 20210329017550 is time: year 2021, month 03, day 29, 01 hour, 75 mins, 50s

## Thread dump

We can get, from the thread dumps