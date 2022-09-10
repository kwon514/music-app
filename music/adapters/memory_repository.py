from typing import List
import csv
from pathlib import Path
from music.adapters import csvdatareader

from music.adapters.csvdatareader import TrackCSVReader
from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.user import User
from music.domainmodel.track import Track
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.playlist import PlayList


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__users = list()
        self.__tracks = list()
        self.__albums = list()
        self.__artists = list()
        self.__genres = list()
        self.__reviews = list()
        self.__playlists = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_track_list(self, track_list: list):
        self.__tracks = track_list

    def add_album_list(self, album_list: list):
        self.__albums = album_list

    def add_artist_list(self, artist_list: list):
        self.__artists = artist_list

    def add_genre_list(self, genre_list: list):
        self.__genres = genre_list

    def get_tracks_by_title(self, track_title: str) -> List[Track]:
        return [track for track in self.__tracks if track.title.lower() == track_title.strip().lower()]

    def get_tracks_by_artist(self, track_artist: str) -> List[Track]:
        return [track for track in self.__tracks if track.artist.full_name.lower() == track_artist.strip().lower()]

    def get_tracks_by_album(self, album_name: str) -> List[Track]:
        return [track for track in self.__tracks if track.album.title.lower() == album_name.strip().lower()]


def populate(data_path: Path, repo: MemoryRepository):
    TrackCSVReader(str(Path(data_path) / 'raw_albums_excerpt.csv'),
                   str(Path(data_path) / 'raw_tracks_excerpt.csv')).read_csv_files()
    repo.add_track_list(TrackCSVReader.dataset_of_tracks)
    repo.add_artist_list(TrackCSVReader.dataset_of_artists)
    repo.add_album_list(TrackCSVReader.dataset_of_albums)
    repo.add_genre_list(TrackCSVReader.dataset_of_genres)
