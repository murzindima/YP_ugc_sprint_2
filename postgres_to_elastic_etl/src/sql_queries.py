GET_MOVIES_SQL = """
SELECT
   fw.id AS "uuid",
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.created,
   fw.modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'uuid', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'actor'),
       '[]'
   ) AS actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'uuid', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'writer'),
       '[]'
   ) AS writers,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'uuid', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id IS NOT NULL AND pfw.role = 'director'),
       '[]'
   ) AS directors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'uuid', g.id,
               'name', g.name,
               'modified', g.modified
           )
       ) FILTER (WHERE g.id IS NOT NULL),
       '[]'
   ) AS genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > %s
GROUP BY fw.id
ORDER BY fw.modified;
"""

msg = """
We assume that any change in the tables of persons or genres triggers a signal in Django 
to update the 'modified' fields of the corresponding movies.
"""

GET_PERSONS_SQL = """
SELECT
    p.id AS "uuid",
    p.full_name,
    p.modified,
    COALESCE(
        json_agg(
            DISTINCT jsonb_build_object(
                'uuid', fw.id,
                'roles', pr.roles
            )
        ) FILTER (WHERE fw.id IS NOT NULL),
        '[]'
    ) AS films
FROM content.person p
LEFT JOIN (
    SELECT
        pfw.person_id,
        pfw.film_work_id,
        array_agg(DISTINCT pfw.role) as roles
    FROM content.person_film_work pfw
    GROUP BY pfw.person_id, pfw.film_work_id
) pr ON pr.person_id = p.id
LEFT JOIN content.film_work fw ON fw.id = pr.film_work_id
WHERE p.modified > %s
GROUP BY p.id
ORDER BY p.modified;
"""

GET_GENRES_SQL = """
SELECT
    g.id AS "uuid",
    g.name,
    g.modified
FROM content.genre g
WHERE g.modified > %s
ORDER BY g.name;
"""
