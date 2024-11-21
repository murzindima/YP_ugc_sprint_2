import uuid

import pytest

from functional.src.conftest import TEST_FILM_UUID, TEST_GENRE_UUIDS, TEST_PERSON_UUIDS


@pytest.fixture
def es_data_films():
    static_film = {
        "uuid": TEST_FILM_UUID,
        "imdb_rating": 9.0,
        "genres": [
            {"uuid": TEST_GENRE_UUIDS["Action"], "name": "Action"},
            {"uuid": TEST_GENRE_UUIDS["Sci-Fi"], "name": "Sci-Fi"},
        ],
        "title": "Test Film Title",
        "description": "Test Film Description",
        "directors": [{"uuid": TEST_PERSON_UUIDS["John Doe"], "name": "John Doe"}],
        "actors": [
            {"uuid": TEST_PERSON_UUIDS["Jane Smith"], "name": "Jane Smith"},
            {"uuid": TEST_PERSON_UUIDS["Alice Johnson"], "name": "Alice Johnson"},
        ],
        "writers": [{"uuid": TEST_PERSON_UUIDS["Bob Brown"], "name": "Bob Brown"}],
    }

    dynamic_films = [
        {
            "uuid": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genres": [
                {"uuid": _genre_uuid, "name": _genre_name}
                for _genre_name, _genre_uuid in TEST_GENRE_UUIDS.items()
            ],
            "title": "The Star" if i < 8 else "X",
            "description": "New World",
            "directors": [
                {"uuid": _person_uuid, "name": _person_name}
                for _person_name, _person_uuid in TEST_PERSON_UUIDS.items()
            ],
            "actors": [
                {"uuid": _person_uuid, "name": _person_name}
                for _person_name, _person_uuid in TEST_PERSON_UUIDS.items()
            ],
            "writers": [
                {"uuid": _person_uuid, "name": _person_name}
                for _person_name, _person_uuid in TEST_PERSON_UUIDS.items()
            ],
        }
        for i in range(59)
    ]

    return [static_film] + dynamic_films


@pytest.fixture
def es_data_genres():
    return [{"uuid": _uuid, "name": _name} for _name, _uuid in TEST_GENRE_UUIDS.items()]


@pytest.fixture
def es_data_persons():
    return [
        {
            "uuid": _uuid,
            "full_name": _name,
            "films": [
                {"uuid": str(uuid.uuid4()), "roles": ["Role " + str(i)]}
                for i in range(5)
            ],
        }
        for _name, _uuid in TEST_PERSON_UUIDS.items()
    ]
