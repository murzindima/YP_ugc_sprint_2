cluster_name = "company_cluster"
database_name = "statistics"
statistics = f"CREATE DATABASE IF NOT EXISTS {database_name} ON CLUSTER {cluster_name}"

table_name = "bookmarks"
bookmarks = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                movie_id UUID,
                description String,
                imdb_rating Float32,
                genres Array(String),
                directors Array(String),
                actors Array(String),
                writers Array(String),
                created_at DATETIME64
            )ENGINE = MergeTree() ORDER BY uuid
            """

table_name = "clicks"
clicks = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                resource String,
                created_at DATETIME64
            )ENGINE = MergeTree() ORDER BY uuid
            """

table_name = "comments"
comments = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                movie_id UUID,
                description String,
                imdb_rating Float32,
                genres Array(String),
                directors Array(String),
                actors Array(String),
                writers Array(String),
                content String,
                created_at DATETIME64
            )ENGINE = MergeTree() ORDER BY uuid
            """

table_name = "likes"
likes = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                movie_id UUID,
                description String,
                imdb_rating Float32,
                genres Array(String),
                directors Array(String),
                actors Array(String),
                writers Array(String),
                created_at DATETIME64
            )ENGINE = MergeTree() ORDER BY uuid
            """

table_name = "movie_filter_requests"
movie_filter_requests = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                filters String,
                created_at DATETIME64
            )ENGINE = MergeTree() ORDER BY uuid
            """

table_name = "movie_player_changes_topic"
movie_player_changes_topic = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                movie_id UUID,
                description String,
                imdb_rating Float32,
                genres Array(String),
                directors Array(String),
                actors Array(String),
                writers Array(String),
                change_type String,
                old_value String,
                new_value String
            )ENGINE = MergeTree() ORDER BY uuid
            """

table_name = "movie_watch_times"
movie_watch_times = f"""CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ON CLUSTER {cluster_name}
             (
                uuid UUID not NULL,
                user_id UUID,
                first_name  String,
                last_name String,
                role_id UUID,
                movie_id UUID,
                description String,
                imdb_rating Float32,
                genres Array(String),
                directors Array(String),
                actors Array(String),
                writers Array(String),
                seconds_amt Int32,
                total_seconds_amt Int32,
                created_at DATETIME64
            )ENGINE = MergeTree() ORDER BY uuid
            """

click_requests = [
    statistics,
    bookmarks,
    clicks,
    comments,
    likes,
    movie_filter_requests,
    movie_watch_times,
    movie_player_changes_topic,
]
