import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from flask_login import current_user, login_required
from builtins import sum

from app_shop import db
from app_shop.models import Game, Cart, Order, User

cart_bp = Blueprint('basket', __name__, template_folder='templates', static_folder='static')


@cart_bp.route('add_basket/<int:game_id>', methods=['POST'])
@login_required
def add_basket(game_id):
    user = current_user

    # Проверьте, существует ли уже игра в корзине пользователя
    cart = Cart.query.filter_by(user_id=user.id, game_id=game_id, order_id=None).first()

    if cart:
        # Игра уже есть в корзине пользователя
        return jsonify({'message': 'The game is already in the basket'}), 400

    # Создайте новый объект Cart
    new_cart = Cart(quantity=1, game_id=game_id, user=user)

    try:
        # Добавьте объект Cart в корзину пользователя
        db.session.add(new_cart)
        db.session.commit()
        return jsonify({'message': 'Game has been successfully added to the basket'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Failed to add the game to the basket'}), 400
    finally:
        db.session.close()


@cart_bp.route('/')
@login_required
def index_basket():
    user = current_user

    # Получите все элементы корзины для текущего пользователя
    cart_items = Cart.query.filter_by(user_id=user.id, order_id=None).all()
    # total_price
    total_price = sum(item.game.price for item in cart_items)

    if total_price > 0:
        # Возвращайте шаблон, передавая в него объекты корзины
        return render_template('basket.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('emty_basket.html', total_price=total_price)


@cart_bp.route('/delete_game', methods=['POST'])
@login_required
def delete_game():
    game_id = request.form.get('game-id')
    user = current_user

    # Find the cart item with the specified game ID for the current user
    cart_item = db.session.query(Cart).filter_by(user_id=user.id, game_id=game_id, order_id=None).first()

    if cart_item:
        try:
            # Remove the cart item from the database
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'message': 'Game deleted from the cart'})
        except:
            db.session.rollback()
            return jsonify({'message': 'Failed to delete the game from the cart'})
        finally:
            db.session.close()
    else:
        return jsonify({'message': 'Cart item not found'})


@cart_bp.route('/pay_basket', methods=['POST'])
@login_required
def pay_basket():
    user = User.query.get(current_user.id)

    # Получите все элементы корзины для текущего пользователя
    cart_items = Cart.query.filter_by(user_id=user.id, order_id=None).all()

    # Рассчитайте общую стоимость товаров в корзине
    total_price = sum(item.game.price for item in cart_items)

    # Проверьте, достаточно ли средств на счету пользователя
    if user.balance is None or user.balance < total_price:
        return jsonify({'message': 'Insufficient funds'})

    try:
        # Создайте новый заказ
        order = Order(total_price=total_price, user=user, status_id=1)
        db.session.add(order)
        db.session.commit()

        # Привяжите корзину к заказу
        for item in cart_items:
            item.order_id = order.id

        # Очистите корзину пользователя
        db.session.query(Cart).filter_by(user_id=user.id, order_id=order.id).delete()

        # Обновите баланс пользователя
        user.balance -= total_price

        db.session.commit()
        return jsonify({'message': 'Payment successful'}), 200
    except:
        db.session.rollback()
        return jsonify({'message': 'Payment failed'}), 400
    finally:
        db.session.close()
