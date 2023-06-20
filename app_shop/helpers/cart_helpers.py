from flask_login import current_user


def inject_cart_count():
    def get_cart_count():
        if current_user.is_authenticated:
            return len(current_user.cart)
        else:
            return 0

    return {'cart_count': get_cart_count}
