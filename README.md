# Crossjoin Thread Dump Analysis

This project contains the code used to analyse the thread dumps provided in the exercise and the interpretation of the extracted data.


## Repository Structure

```
code/
```

Python scripts that parse the thread dumps and generate CSV files containing the extracted information.

```
data/
```

Input and output data for the analysis. Only the diagrams are exposed in the repository.

```
exercise/
```

Documentation related to the exercise, including the study, findings, and conclusions.

## Conlusion

The problem simply seems to be a scarcity of jolt sessions, which create a bottleneck at `borrowSession`.

If possible, these sessions should be increased. Another solution would be increasing the number of instances of the base service.