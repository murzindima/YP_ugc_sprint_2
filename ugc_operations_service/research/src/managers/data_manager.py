import os
from datetime import datetime
from random import choices, randint
from uuid import uuid4

from faker import Faker
from tqdm.asyncio import tqdm

from helpers import logger
from managers.csv_manager import CSVManager

fake = Faker()


class DataManager:
    """Class for generating initial data for movies, users, and reviews."""

    def __init__(
        self,
        movies_amount=100_000,
        users_amount=1_000_000,
        each_type_of_events_amount=3_000_000,
    ):
        self.csv_manager = CSVManager()
        self.movies_amount = movies_amount
        self.users_amount = users_amount
        self.each_type_of_events_amount = each_type_of_events_amount
        self.batch_size = 50_000

    async def generate_initial_data(self):
        movies_ids = tuple(str(uuid4()) for _ in range(self.movies_amount))
        users_ids = tuple(str(uuid4()) for _ in range(self.users_amount))

        step = min(self.batch_size, max(self.movies_amount, self.users_amount))
        for i in range(0, self.each_type_of_events_amount, step):
            movies_ids_sample = choices(movies_ids, k=step)
            users_ids_sample = choices(users_ids, k=step)

            yield movies_ids_sample, users_ids_sample

    @staticmethod
    async def create_likes(
        movies_ids_sample: list[str], users_ids_batch: list[str]
    ) -> list[tuple]:
        likes = []
        for movie_id, user_id in zip(movies_ids_sample, users_ids_batch):
            likes.append((user_id, movie_id, 10, datetime.now()))
        return likes

    @staticmethod
    async def create_reviews(
        movies_ids_sample: list[str], reviewers_ids_batch: list[str]
    ) -> list[tuple]:
        reviews = []
        for movie_id, reviewer_id in zip(movies_ids_sample, reviewers_ids_batch):
            reviews.append(
                (
                    reviewer_id,
                    movie_id,
                    fake.text(max_nb_chars=20),
                    randint(0, 10),
                    datetime.now(),
                )
            )
        return reviews

    @staticmethod
    async def create_bookmarks(
        movies_ids_sample: list[str], users_ids_batch: list[str]
    ) -> list[tuple]:
        bookmarks = []
        for movie_id, user_id in zip(movies_ids_sample, users_ids_batch):
            bookmarks.append((user_id, movie_id, datetime.now()))
        return bookmarks

    async def save_initial_data_to_csv(self):
        async for movies_ids_sample, users_ids_batch in tqdm(
            self.generate_initial_data()
        ):
            likes = await self.create_likes(movies_ids_sample, users_ids_batch)
            reviews = await self.create_reviews(movies_ids_sample, users_ids_batch)
            bookmarks = await self.create_bookmarks(movies_ids_sample, users_ids_batch)

            await self.csv_manager.write_to_csv(
                file_path="data/likes.csv", records=likes
            )
            await self.csv_manager.write_to_csv(
                file_path="data/reviews.csv", records=reviews
            )
            await self.csv_manager.write_to_csv(
                file_path="data/bookmarks.csv", records=bookmarks
            )

        logger.info("CSV files filled successfully.")

    @staticmethod
    async def clear_directory_with_data(folder="data"):
        current_file_path = os.getcwd()
        data_path = os.path.join(current_file_path, folder)
        files = os.listdir(data_path)
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(data_path, file)
                os.remove(file_path)
                logger.info(f"File {file} removed successfully.")
