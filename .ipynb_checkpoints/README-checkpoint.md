Instructions for run the project:
1 - Swap database credentials with your local database credentials
2 - Run the create_tables.py file
3 - Run the etl.py file
4 - (Optional) Change credentials and use the test.ipynb file


Questions from udacity about the project
1. Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
This database may provide us with important information about songs, artists and users who use our platform. With the queries that I will write below, it is possible to analyze specific information and build new features within the platform and adapt it to each user's profile. Thus, the analysis of this data becomes important to update our products, analyze what has the greatest reach in the music market, adapt our product to different user profiles and keep our users on the platform with more personalized services.
    
2. State and justify your database schema design and ETL pipeline.
Schema:
    For the development of the project, we followed the scheme provided in the project instructions, which centralizes as a fact the execution of a song within the platform and uses information from users, music, artists and time as dimensions. This denormalized model represents the star schema model and is interesting because it allows us to consult important information about our users' tastes, artists and music in a fast, efficient and business-oriented way.
    
ETL:
    This stage of the project was divided into the following stages:
    Step 1: Extracting data from json files, transforming and loading into the artist and song dimension tables.
    Step 2: Extracting data from json files from the music play logs, transforming and loading into the user-time dimension tables and the songplays fact table.
    
3. [Optional] Provide example queries and results for song play analysis.


What are the most listened to songs?
SELECT s.title, COUNT(*) as playsBySong
	FROM songplays sp
	INNER JOIN songs s
	ON sp.song_id = s.song_id
group by s.song_id;


Which artists are the most listened to?
SELECT a.name, COUNT(*) as playsByArtist
	FROM songplays sp
	INNER JOIN artists as a
	ON sp.artist_id = a.artist_id
group by a.artist_id;


Which browser is our app most accessed through?
SELECT user_agent, COUNT(*) playsByNavigator 
	FROM songplays
GROUP BY user_agent;

What are the locations with the highest number of music reproductions?
SELECT location, COUNT(*) playsByLocation 
	FROM songplays
GROUP BY location;


What are the locations with the highest number of music reproductions?
SELECT s.year, COUNT(*) as numberOfSongs
	FROM songplays sp
	INNER JOIN songs s
	ON sp.song_id = s.song_id
group by s.year;

What are the most listened to songs by gender?
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

SELECT date(t.start_time) date_play, count(*) numberOfPlays
	FROM songplays sp 
	INNER JOIN time t 
	ON sp.start_time = t.start_time
GROUP BY date(t.start_time);



Note: For some of these analyzes it would be necessary to update the artist and music dimension tables with the log table records



What are the most listened to artists by genre?

SELECT a.name, COUNT(*) as playsByGender
	FROM songplays sp
	INNER JOIN artists a
	ON sp.artist_id = a.artist_id
	
	INNER JOIN users u
	on sp.user_id = u.user_id
WHERE gender = 'F'
group by a.artist_id;

SELECT a.name, COUNT(*) as playsByGender
	FROM songplays sp
	INNER JOIN artists a
	ON sp.artist_id = a.artist_id
	
	INNER JOIN users u
	on sp.user_id = u.user_id
WHERE gender = 'M'
group by a.artist_id;



Music plays per day
SELECT date(t.start_time) date_play, count(*) numberOfPlays
	FROM songplays sp 
	INNER JOIN time t 
	ON sp.start_time = t.start_time
GROUP BY date(t.start_time);