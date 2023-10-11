from django.apps import AppConfig


class GroupchatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'groupchat'

    def ready(self):
        import groupchat.signals
