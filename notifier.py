from plyer import notification
def send_notification(title, message):
    notification.notify(
        app_name='News Notifier',
        title=title,
        message=message,
        timeout=10  # Display duration in seconds
    )