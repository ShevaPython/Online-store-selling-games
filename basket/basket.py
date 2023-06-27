import base64
import json

from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify
)
from flask_login import current_user, login_required
from sqlalchemy import or_
from builtins import sum

from liqpay import LiqPay
from .verify_callback import verify_callback_data

from app_shop import db
from app_shop.models import  Cart, Order, User
import config


cart_bp = Blueprint('basket', __name__, template_folder='templates', static_folder='static')

# Создайте экземпляр класса LiqPay
liqpay = LiqPay(config.LIQPAY_PUBLIC, config.LIQPAY_PRIVATE)


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
    cart_items = Cart.query.filter_by(user_id=user.id).filter(or_(Cart.order_id == None,
                                                                  Cart.order_id != None)).all()
    # total_price
    total_price = sum(item.game.price for item in cart_items)

    if total_price > 0:
        # Возвращайте шаблон, передавая в него объекты корзины
        return render_template('basket.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('empty_basket.html', total_price=total_price)


@cart_bp.route('/delete_game', methods=['POST'])
@login_required
def delete_game():
    game_id = request.form.get('game-id')
    user = current_user

    # Find the cart item with the specified game ID for the current user
    cart_item = db.session.query(Cart).filter_by(user_id=user.id, game_id=game_id).filter(
        or_(Cart.order_id == None,
            Cart.order_id != None)).first()

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


@cart_bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    user = User.query.get(current_user.id)

    # Получите все элементы корзины для текущего пользователя
    cart_items = Cart.query.filter_by(user_id=user.id).filter(or_(Cart.order_id == None,
                                                                  Cart.order_id != None)).all()
    # total_price
    total_price = sum(item.game.price for item in cart_items)

    if request.method == 'POST':
        try:
            # Создайте новый заказ
            order = Order(total_price=total_price, user=user, status_id=2)
            db.session.add(order)
            db.session.commit()

            # Привяжите корзину к заказу
            for item in cart_items:
                item.order_id = order.id

            # # Очистите корзину пользователя
            # db.session.query(Cart).filter_by(user_id=user.id, order_id=order.id).delete()
            # db.session.commit()

            params = {
                "action": "pay",
                "amount": str(total_price),
                "currency": "UAH",
                "description": 'Text',
                "order_id": str(order.id),
                "version": "3",
                "result_url": url_for('basket.liqpay_callback', _external=True)
            }
            form = liqpay.cnb_form(params)
            return render_template('payment.html', cart_items=cart_items, total_price=total_price, form=form)

        except:
            db.session.rollback()

        finally:
            db.session.close()

    # Если метод запроса GET, просто отображаем содержимое корзины
    return redirect(url_for('basket.index_basket'))


@cart_bp.route('/liqpay_callback', methods=['POST'])
def liqpay_callback():
    data = request.form.get('data')
    signature = request.form.get('signature')
    private_key = config.LIQPAY_PRIVATE
    if verify_callback_data(data, signature, private_key):
        decoded_data = base64.b64decode(data).decode('utf-8')
        callback_data = json.loads(decoded_data)
        # Отримайте статус платежу з callback_data
        payment_status = callback_data.get('status')

        if payment_status == 'success':
            # Платіж успішний, виконайте необхідні дії
            # Наприклад, оновіть статус замовлення в базі даних

            return 'OK'
        elif payment_status == 'failure':
            # Платіж не вдалося, виконайте необхідні дії

            return 'OK'
        else:
            # Інший статус платежу, виконайте відповідні дії



            return render_template('callback.html', data=callback_data, signature=signature)
