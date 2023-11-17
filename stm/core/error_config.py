from handlers.error_handlers.common import HANDLERS

def setup_error_handlers(app):
  for exc_class, handler in HANDLERS:
    app.add_exception_handler(exc_class, handler)

