from http import HTTPStatus
from json import JSONDecodeError

from core.config import authorizations, app_settings
from core.logger_class import Logger
from flask import Response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields
from schemas.bookmark import Bookmark
from schemas.click import Click
from schemas.comment import Comment
from schemas.like import Like
from schemas.movie_filter_request import MovieFilterRequest
from schemas.movie_player_change import MoviePlayerChange

from app.core.config import kafka_settings
from app.schemas.movie_watch_time import MovieWatchTime
from app.services.kafka import KafkaProducerService

kafka_producer_service = KafkaProducerService()

events_namespace = Namespace(
    "events", description="Operations related to events", authorizations=authorizations
)

movie_watch_time_model = events_namespace.model(
    name="MovieWatchTime",
    model={
        "movie_id": fields.String(),
        "seconds_amt": fields.Integer(),
        "total_seconds_amt": fields.Integer(),
        "created_at": fields.DateTime(),
    },
)
click_model = events_namespace.model(
    name="Click", model={"resource": fields.String(), "created_at": fields.DateTime()}
)
bookmark_model = events_namespace.model(
    name="Bookmark", model={"movie_id": fields.String()}
)
like_model = events_namespace.model(
    name="Like",
    model={
        "movie_id": fields.String(),
        "resource": fields.String(),
        "created_at": fields.DateTime(),
    },
)
comment_model = events_namespace.model(
    name="Comment",
    model={
        "movie_id": fields.String(),
        "content": fields.String(),
        "created_at": fields.DateTime(),
    },
)
movie_player_change_model = events_namespace.model(
    name="MoviePlayerChange",
    model={
        "movie_id": fields.String(),
        "change_type": fields.String(),
        "old_value": fields.String(),
        "new_value": fields.String(),
    },
)
movie_filter_request_model = events_namespace.model(
    name="MovieFilterRequest", model={"filters": fields.String()}
)

logger = Logger(app_settings.log_path, app_settings.level)


@events_namespace.route("/movie-watch-time")
class MovieWatchTimeAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(movie_watch_time_model)
    def post(self):
        """Sends movie timestamp to Kafka."""

        logger.write_log(
            messages="MovieWatchTimeAPI", request_id=request.headers.get("X-Request-Id")
        )
        movie_watch_time = MovieWatchTime(**request.get_json())
        movie_watch_time.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.movie_watch_times_topic,
            message=movie_watch_time.model_dump_json(),
            key=movie_watch_time.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)


@events_namespace.route("/click")
class ClickAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(click_model)
    def post(self):
        """Sends user's click to Kafka."""

        logger.write_log(
            messages="ClickAPI", request_id=request.headers.get("X-Request-Id")
        )
        click = Click(**request.get_json())
        click.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.clicks_topic,
            message=click.model_dump_json(),
            key=click.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)


@events_namespace.route("/like")
class LikeAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(like_model)
    def post(self):
        """Sends user's like information to Kafka."""

        logger.write_log(
            messages="LikeAPI", request_id=request.headers.get("X-Request-Id")
        )
        like = Like(**request.get_json())
        like.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.likes_topic,
            message=like.model_dump_json(),
            key=like.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)


@events_namespace.route("/comment")
class CommentAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(comment_model)
    def post(self):
        """Sends user's comment to Kafka."""

        logger.write_log(
            messages="CommentAPI", request_id=request.headers.get("X-Request-Id")
        )
        comment = Comment(**request.get_json())
        comment.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.comments_topic,
            message=comment.model_dump_json(),
            key=comment.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)


@events_namespace.route("/bookmark")
class BookmarkAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(bookmark_model)
    def post(self):
        """Sends user's bookmark to Kafka."""

        logger.write_log(
            messages="BookmarkAPI", request_id=request.headers.get("X-Request-Id")
        )
        bookmark = Bookmark(**request.get_json())
        bookmark.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.bookmarks_topic,
            message=bookmark.model_dump_json(),
            key=bookmark.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)


@events_namespace.route("/movie-filter-request")
class MovieFilterRequestAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(movie_filter_request_model)
    def post(self):
        """Sends user's movie filter request to Kafka."""

        logger.write_log(
            messages="MovieFilterRequestAPI",
            request_id=request.headers.get("X-Request-Id"),
        )
        try:
            movie_filter_request = MovieFilterRequest.from_json(**request.get_json())
        except JSONDecodeError:
            return Response("Wrong json for filters key", status=HTTPStatus.BAD_REQUEST)

        movie_filter_request.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.movie_filter_requests_topic,
            message=movie_filter_request.model_dump_json(),
            key=movie_filter_request.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)


@events_namespace.route("/movie-player-change")
class MoviePlayerChangeAPI(Resource):
    method_decorators = [jwt_required(optional=True)]

    @events_namespace.doc(security="jsonWebToken")
    @events_namespace.expect(movie_player_change_model)
    def post(self):
        """Sends user's movie language change request."""

        logger.write_log(
            messages="MoviePlayerChangeAPI",
            request_id=request.headers.get("X-Request-Id"),
        )
        movie_player_change = MoviePlayerChange(**request.get_json())
        movie_player_change.user_id = get_jwt_identity()

        kafka_producer_service.produce_message(
            topic=kafka_settings.movie_player_changes_topic,
            message=movie_player_change.model_dump_json(),
            key=movie_player_change.user_id or "Anonymous",
        )

        return Response(status=HTTPStatus.OK)
