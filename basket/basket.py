import base64
import json

from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify
)
from flask_mail import Message
from flask_login import current_user, login_required
from sqlalchemy import or_
from builtins import sum

from liqpay import LiqPay


from .verify_callback import verify_callback_data

from app_shop import db, mail
from app_shop.models import Cart, Order, User, Status, Game
import config

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
    cart_items = Cart.query.filter_by(user_id=user.id,order_id=None).all()
    if cart_items:
    # total_price
        total_price = sum(item.game.price for item in cart_items)

        if request.method == 'POST':
            try:
                unpaid_status = Status.query.filter_by(name='unpaid').first()
                if not unpaid_status:
                    unpaid_status = Status(name='unpaid')
                    db.session.add(unpaid_status)
                    db.session.commit()

                order = Order(total_price=total_price, user=user, status_id=unpaid_status.id)
                db.session.add(order)
                db.session.commit()


                # Привяжите корзину к заказу
                for item in cart_items:
                    item.order_id = order.id

                db.session.commit()

                #экземпляр класса LiqPay
                liqpay = LiqPay(config.LIQPAY_PUBLIC, config.LIQPAY_PRIVATE)

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

    Cart.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    return redirect(url_for('basket.index_basket'))


@cart_bp.route('/liqpay_callback', methods=['POST'])
@login_required
def liqpay_callback():
    user_id = current_user.id
    current_email = current_user.email
    data = request.form.get('data')
    signature = request.form.get('signature')
    private_key = config.LIQPAY_PRIVATE

    if not verify_callback_data(data, signature, private_key):
        return 'Unauthorized', 401

    decoded_data = base64.b64decode(data).decode('utf-8')
    callback_data = json.loads(decoded_data)
    payment_status = callback_data.get('status')
    success_order = callback_data.get('order_id')

    if payment_status == 'success':
        try:
            order = Order.query.get(int(success_order))
            if not order:
                raise ValueError('Invalid order ID')

            paid_status = Status.query.filter_by(name='paid').first()
            if not paid_status:
                paid_status = Status(name='paid')
                db.session.add(paid_status)
                db.session.commit()

            order.status_id = paid_status.id
            db.session.commit()

            game_cart_items = Cart.query \
                .filter_by(user_id=user_id, order_id=int(success_order)) \
                .join(Game) \
                .with_entities(
                Game.photo,
                Game.name,
                Game.activation_key
            ) \
                .all()
            try:
                html_template = render_template('send_key_game.html',game=game_cart_items)

                # Отправка письма
                msg = Message('Ваша покупка', recipients=[current_email],html=html_template)
                mail.send(msg)
            except Exception as e:
                print(f"Error sending email: {str(e)}")

            db.session.query(Cart).filter_by(user_id=user_id, order_id=order.id).delete()
            db.session.commit()

            return render_template('callback.html', callback_data=callback_data)
        except Exception as e:
            db.session.rollback()
            return str(e), 500
        finally:
            db.session.close()

    elif payment_status == 'failure':
        try:
            order = Order.query.get(int(success_order))
            if not order:
                raise ValueError('Invalid order ID')

            db.session.query(Cart).filter_by(user_id=user_id, order_id=order.id).delete()
            db.session.commit()

            return render_template('callback.html', callback_data=callback_data)
        except Exception as e:
            db.session.rollback()
            return str(e), 500
        finally:
            db.session.close()

    else:
        try:
            order = Order.query.get(int(success_order))
            if not order:
                raise ValueError('Invalid order ID')

            db.session.query(Cart).filter_by(user_id=user_id, order_id=order.id).delete()
            db.session.commit()

            return render_template('callback.html', callback_data=callback_data)
        except Exception as e:
            db.session.rollback()
            return str(e), 500
        finally:
            db.session.close()

