from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)


from app_shop import db
from app_shop.models import Game

card_bp = Blueprint('basket', __name__, template_folder='templates', static_folder='static')


@card_bp.route('/')
def index_basket():
    games = Game.query.all()
    return  render_template('basket.html',games=games)
