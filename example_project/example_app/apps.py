from django.apps import AppConfig


class ExampleAppConfig(AppConfig):
    name = 'example_app'

    def ready(self):
        import example_app.signals