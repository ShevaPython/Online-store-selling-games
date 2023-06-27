def inject_genres():
    """контекстный процесс на взятие всех жанров"""
    from app_shop.models import Genre
    def get_genres():
        return Genre.query.all()

    return {'genres': get_genres}
