from django.apps import AppConfig


class ComptesConfig(AppConfig):
    name = 'comptes'

    def ready(self):
        import comptes.signals
