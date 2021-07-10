# Sparkify Data pipeline
--- 
**This project is part of module 1 of udacity's data engineering course - relational databases, star schema and snow flake modeling.**

Pipeline for extracting, transforming, and loading data from the sparkify music streaming app into a database for analytics.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Files](#files)
* [Setup](#setup)
* [Code example](#code-example)

## General info
A startup called Sparkify wants to analyze the data they’ve been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to.
This project performs the extraction and transformation of data coming from user logs and music plays from sparkify's music streaming app. In addition, we carry out the modeling of a dimensional database using star schema modeling. Finally, the project loads the transformed data in this database for further analysis of this information. The image below shows the data model.

![starschema](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/339318/1586016120/Song_ERD.png)


## Technologies
The project is created with:
* Python version: 3.8.8
* Jupyter lab: 3.0.14
* Pandas module version: 1.2.4
* PostgreSQL version: 13
* psycopg2 (postgres) module version: 2.9.1

## Files
The project contains this files
* sql_queries.py: this file contains the instructions for creating the database in PostgreSQL 13 and defines the SQL queries.
* create_tables.py: this file contains the code responsible for create of the database and tables.
* etl.py: This file contains the code responsible for extracting data from data sources, transforming them and loading them into the database.
* test.ipynb: This file contains the code responsible for testing the previous codes on some development platforms, such as the jupyter lab.

## Setup
To run this project locally:

```
$ cd ../[project directory path]
$ python create_tables.py
$ python etl.py
``` 
    
## Code examples

Database queries: 
1. What are the most played songs?
```
SELECT s.title, COUNT(*) as playsBySong
	FROM songplays sp
	INNER JOIN songs s
	ON sp.song_id = s.song_id
group by s.song_id;
```


2. Which artists are the most listened to?
```
SELECT a.name, COUNT(*) as playsByArtist
	FROM songplays sp
	INNER JOIN artists as a
	ON sp.artist_id = a.artist_id
group by a.artist_id;
```


3. What is the most used browser?
```
SELECT user_agent, COUNT(*) playsByNavigator 
	FROM songplays
GROUP BY user_agent;
```

4. What are the locations with the highest number of music plays?
```
SELECT location, COUNT(*) playsByLocation 
	FROM songplays
GROUP BY location;
```


5. What are the locations with the highest number of music plays?
```
SELECT s.year, COUNT(*) as numberOfSongs
	FROM songplays sp
	INNER JOIN songs s
	ON sp.song_id = s.song_id
group by s.year;
```


6. What are the most listened to songs by gender?

```
SELECT s.title, COUNT(*) as playsBySong
	FROM songplays sp
	INNER JOIN songs s
	ON sp.song_id = s.song_id
	
	INNER JOIN users u
	on sp.user_id = u.user_id
WHERE gender = 'F'
group by s.song_id;

SELECT s.title, COUNT(*) as playsBySong
	FROM songplays sp
	INNER JOIN songs s
	ON sp.song_id = s.song_id
	
	INNER JOIN users u
	on sp.user_id = u.user_id
WHERE gender = 'M'
group by s.song_id;
```