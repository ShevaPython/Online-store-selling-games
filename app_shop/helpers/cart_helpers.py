from flask_login import current_user


def inject_cart_count():
    """контекстный процесс на взятие количество заказов"""
    def get_cart_count():
        if current_user.is_authenticated:
            return current_user.cart.count()
        else:
            return 0

    return {'cart_count': get_cart_count}
