def inject_genres():
    from app_shop.models import Genre
    def get_genres():
        return Genre.query.all()

    return {'genres': get_genres}
