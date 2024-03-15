from django.apps import AppConfig


class PainterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'painter'
    def ready(self):
        print("Server started")
        pass  # startup code here
