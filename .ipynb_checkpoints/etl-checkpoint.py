import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
        Proccess song file and insert artists and song into their respective dimension tables
        :param cur: cursor of database
        :param filepath string: path of root directory of files
    """
    # open song file
    df = pd.DataFrame([pd.read_json(filepath, typ='series')])

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e:
        print('Error: Could not execute query to insert songs')
        print(e)
    
    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e:
        print('Error: Could not execute query to insert artists')
        print(e)


def process_log_file(cur, filepath):
    """
        Proccess log file and insert users and times into their respective dimension tables and insert song plays into fact table
        :param cur: cursor of database
        :param filepath string: path of root directory of files
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query("page=='NextSong'")

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    df['timestamp'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df =  pd.DataFrame(dict(zip(column_labels,time_data)))
    try:
        for i, row in time_df.iterrows():
            cur.execute(time_table_insert, list(row))
    except psycopg2.Error as e:
        print('Error: Could not execute query to insert times')
        print(e)

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender','level']]
    

    # insert user records
    try:
        for i, row in user_df.iterrows():
            cur.execute(user_table_insert, row)
    except psycopg2.Error as e:
        print('Error: Could not execute query to insert users')
        print(e)

    
    # insert songplay records
    try:
        for index, row in df.iterrows():
            # get songid and artistid from song and artist tables
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()

            if results:
                songid, artistid = results
            else:
                songid, artistid = None, None

            # insert songplay record
            songplay_data = (row.timestamp, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
            cur.execute(songplay_table_insert, songplay_data)
    except psycopg2.Error as e:
        print('Error: Could not execute query to get artist_id and song_id ou insert data into songplays')
        print(e)


def process_data(cur, conn, filepath, func):
    """
        Proccess the datasets.
        :param cur: cursor of database
        :param conn: database connections
        :param filepath string: path of root directory of files
        :param func: function to treatament each specific type of data
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
        cur = conn.cursor()
    except psycopg2.Error as e:
        print('Error: Could not to get database connection or cursor')
        print(e)

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()
    


if __name__ == "__main__":
    main()