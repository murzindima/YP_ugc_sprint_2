from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, PersonFilmwork, Person


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "modified")
    search_fields = ("name", "description")


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created",
        "modified",
    )
    list_filter = ("type", "creation_date", "rating")
    search_fields = ("title", "type", "description")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "created", "modified")
    search_fields = ("full_name",)
