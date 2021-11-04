import string
import random
from models import setup_db, Gender, Casting, Actor, Movie


def prepare_movies():
    Movie.query.delete()
    seed_movie = Movie(title="The Girl with the Dragon Tattoo", release_date="2011-12-20")
    seed_movie.insert()
    seed_movie.apply()
    seed_movie.delete()
    return True

def generate_movie():
    title = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))
    movie = Movie(title=title, release_date="2001-01-01T00:00:00.511Z")
    movie.insert()
    movie.apply()
    movie.refresh()
    return movie
