from django.apps import AppConfig


class AstromallConfig(AppConfig):
    name = 'astromall'

    def ready(self):
        import astromall.admin_panel
