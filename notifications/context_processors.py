from .models import Notification

def notifications_context(request):
    # अगर user login नहीं है तो कुछ मत भेजो
    if not request.user.is_authenticated:
        return {}

    unread_count = Notification.objects.filter(is_read=False).count()
    return {
        "notif_unread_count": unread_count
    }
