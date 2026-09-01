# /experiment Command

Design and execute experiments to test hypotheses.

## Usage

```
/experiment <hypothesis or question>
```

## Behavior

1. Formulates the hypothesis
2. Designs distinguishing experiments
3. Considers cost and information value
4. Executes experiments
5. Observes results
6. Updates confidence

## Examples

```
/experiment The memory leak is caused by the connection pool not releasing idle connections
/experiment Adding a cache layer will reduce p99 latency by at least 30%
/experiment The bug only manifests when using the PostgreSQL driver
```
