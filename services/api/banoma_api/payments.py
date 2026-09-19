"""Intégrations de paiement — Stripe (cartes) et Mobile Money (Orange/Moov)."""
import os
import stripe

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')


def create_stripe_checkout_session(amount: int, currency: str, success_url: str, cancel_url: str):
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currency,
                'product_data': {'name': 'Prestation BANOMA'},
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )


def charge_mobile_money(phone: str, amount: int):
    """Squelette Mobile Money (Orange Money / Moov Money au Burkina Faso).
    À brancher sur l'API du fournisseur retenu — pour l'instant renvoie un statut
    'queued' simulé afin de ne pas bloquer le flux MVP tant que le contrat n'est pas signé."""
    client_id = os.environ.get('MOBILE_MONEY_CLIENT_ID')
    if not client_id:
        return {'status': 'queued', 'reference': None}
    # TODO: implémentation réelle une fois le fournisseur choisi
    return {'status': 'queued', 'reference': None}
