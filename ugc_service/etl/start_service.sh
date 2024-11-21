python ./create_schema.py

python ./ETL.py bookmarks &
python ./ETL.py clicks &
python ./ETL.py comments &
python ./ETL.py likes &
python ./ETL.py movie_filter_requests &
python ./ETL.py movie_player_changes_topic &
python ./ETL.py movie_watch_times