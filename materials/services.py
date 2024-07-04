import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product):
    """Создает продукт в страйпе"""
    product = stripe.Product.create(name=product.title)
    return product.get("id")


def create_stripe_price(amount, product):
    """Создает цену в страйпе"""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
        product=product,
    )
    return price.get("id")


def create_stripe_session(price):
    """Создает сессию в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
