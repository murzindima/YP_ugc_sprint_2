# MongoDB VS Postgres Research

## Set up the Databases

```shell
docker-compose -f ugc_operations_service/research/docker-compose.yml
```

## Execute the Scripts

```shell 
python3 ugc_operations_service/research/src/prepare_databases.py
```

```shell
python3 ugc_operations_service/research/src/run_operations.py
```

```shell
python3 ugc_operations_service/research/src/show_results.py
```

## Description

### Number of objects:

- Users: 1M
- Movies: 100K
- Likes: 3M
- Reviews: 3M
- Bookmarks: 3M

### Tests conducted:

1) Additional records write time
2) Retrieving movies liked by a user
3) Retrieving movies bookmarked by a user
4) Retrieving movie's likes and dislikes amount
5) Calculating the average user rating for a movie

Each test is performed 100 times

![image](Figure_1.png)


## Conclusions
The write operations for new data proved to be faster in MongoDB, while the read operations were more efficient in PostgreSQL. 
Overall, both databases meet the speed requirements for operations within 200 ms, being faster than the limit by more than 10 times.
It is worth noting that results may vary depending on hardware characteristics and database configurations,
however, even with the addition of simple indexes, high speed was achieved with fairly large datasets.
