import os
from unittest import mock

os.environ["MODE"] = "TEST"

mock.patch(
    'fastapi_cache.decorator.cache', lambda *args, **kwargs: lambda f: f
).start()

mock.patch(
    'app.tasks.tasks.send_booking_confirmation_email.delay', lambda *args, **kwargs: lambda f: f
).start()
