def verify_callback_data(data, signature, private_key):
    import base64
    import hashlib
    # Розкодування параметру data з base64
    decoded_data = base64.b64decode(data).decode('utf-8')

    # Формування підпису на стороні сервера
    signature_to_check = base64.b64encode(
        hashlib.sha1((private_key + data + private_key).encode('utf-8')).digest()).decode('utf-8')

    # Порівняння підписів
    if signature == signature_to_check:
        return True
    else:
        return False