# lib/logger.py

application_ui_ref = None

def set_ui_logger(app_ui_instance):
    global application_ui_ref
    application_ui_ref = app_ui_instance

def log(message):
    print(message)
    if application_ui_ref:
        try:
            application_ui_ref._append_to_console(message)
        except Exception as e:
            print(f"[Logger Warning] UI log failed: {e}")

def clear_log():
    if application_ui_ref:
        try:
            application_ui_ref._clear_console()
        except Exception as e:
            print(f"[Logger Warning] UI clear failed: {e}")
