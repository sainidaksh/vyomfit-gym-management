# core/context_processors.py
"""
Context processor to provide unread notifications count per authenticated user.
Always returns the same key 'notif_unread_count' for template consistency.
"""

from notifications.models import Notification

def notifications_context(request):
    """
    Return {'notif_unread_count': <int>} for authenticated users,
    and {'notif_unread_count': 0} for anonymous users.
    """
    if not request.user.is_authenticated:
        return {"notif_unread_count": 0}

    try:
        # If your Notification model uses a different FK name (like 'recipient'), change 'user' below.
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
    except Exception:
        # Fallback to 0 if DB not available or field name differs
        unread = 0
    return {"notif_unread_count": unread}
