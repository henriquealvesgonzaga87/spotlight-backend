from frameworks_drivers.fastapi.app import App
from interface_adapters.api.user_routes import router as user_routes
from settings import get_settings


settings = get_settings()
app = App.get_app(settings=settings, router=user_routes)
