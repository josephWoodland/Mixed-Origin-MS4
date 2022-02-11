from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "checkout"

    def ready(self):
        # Connect the signals to the app
        import checkout.signals
