# Databases-Lab-CS-345
Implementation of Databases Assignments in Lab CS-345

1. To import large data in mysql, 'set autocommit=0' to perform each query without actually commiting them. This commits queries at last when the session closes, hence making import faster.

2. While viewing tables in cassandra use 'EXPAND ON' to view tables vertically.

3. Neo4j processing slows down if we use 'merge' statement more often. It's how the merge statement works. Hence we should try to use it minimally.
