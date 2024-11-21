import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("id")
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class FilmworkType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255, db_index=True)
    description = models.TextField(_("description"), null=True)
    creation_date = models.DateField(_("creation_date"), null=True, db_index=True)
    rating = models.FloatField(
        _("rating"),
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        db_index=True,
    )
    type = models.CharField(
        _("type"),
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
        max_length=7,
    )
    genres = models.ManyToManyField(
        Genre, through="GenreFilmwork", verbose_name=_("genres")
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = "Кинопроизведение"
        verbose_name_plural = "Кинопроизведения"


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = "Жанр кинопроизведения"
        verbose_name_plural = "Жанры кинопроизведения"
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "genre_id"], name="film_work_genre"
            )
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255, db_index=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = "Персона"
        verbose_name_plural = "Персоны"


class PersonFilmworkRole(models.TextChoices):
    ACTOR = "actor", _("actor")
    WRITER = "writer", _("writer")
    DIRECTOR = "director", _("director")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("film_work")
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    role = models.CharField(
        _("role"),
        choices=PersonFilmworkRole.choices,
        default=PersonFilmworkRole.ACTOR,
        max_length=8,
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = "Актер кинопроизведения"
        verbose_name_plural = "Актеры кинопроизведения"
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_role",
            )
        ]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} {self.id}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label = "movies"
