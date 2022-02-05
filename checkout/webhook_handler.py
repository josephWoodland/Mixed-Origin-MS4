from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from products.models import Product
from django.core.mail import send_mail
from django.template.loader import render_to_string
from profiles.models import Profile, Wallet
from .models import Order, OrderItem
from django.conf import settings

import uuid
import json
import time


class StripeWH_Handler:
    def __init__(self, request):
        self.request = request

    def _send_conformation_email(self, order):
        customer_email = order.email

        subject = render_to_string(
            "checkout/confirmation_emails/confirmation_email_subject.txt",
            {"order": order},
        )
        body = render_to_string(
            "checkout/confirmation_emails/confirmation_email_body.txt",
            {"order": order, "contact_email": settings.DEFAULT_FROM_EMAIL},
        )

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [customer_email])

    def handle_event(self, event):

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_succeeded(self, event):

        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        walletDetails = intent.metadata.walletDetails
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping

        grand_total = round(intent.charges.data[0].amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username

        if username != "AnonymousUser":
            profile = Profile.objects.get(username=username)
            wallet = Wallet.objects.get(owner=profile)
            full_name = profile.first_name + " " + profile.second_name

            if walletDetails:
                wallet.name = full_name
                wallet.phone_number = shipping_details.phone
                wallet.country = shipping_details.address.country
                wallet.postcode = shipping_details.address.postal_code
                wallet.town_or_city = shipping_details.address.city
                wallet.street_address1 = shipping_details.address.line1
                wallet.street_address2 = shipping_details.address.line2
                wallet.county = shipping_details.address.state
                wallet.save()

        order_exists = False

        attempt = 1
        while attempt <= 5:

            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    stripe_pid=pid,
                )

                order_exists = True
                break

            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_conformation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]}| SUCCESS: Verified order already in database',
                status=200,
            )

        else:
            order = None

            try:
                id_number = uuid.uuid4()
                id = str(id_number)

                order = Order.objects.create(
                    full_name=shipping_details.name,
                    profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    stripe_pid=pid,
                    id=id,
                )

                order.save()

                for item_id, quantity in json.loads(cart).items():
                    product = get_object_or_404(Product, pk=item_id)
                    item_total = product.price * quantity

                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        item_total=item_total,
                    )

                    order_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500,
                )

        self._send_conformation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}| SUCCESS: Verified order already in database',
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):

        return HttpResponse(content=f'Webhook received: {event["type"]}', status=200)
