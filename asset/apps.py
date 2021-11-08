from django.apps import AppConfig


class AssetConfig(AppConfig):
    name = 'asset'
    
    def ready(self):
        import asset.signals
