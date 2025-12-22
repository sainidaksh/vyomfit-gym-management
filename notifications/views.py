from datetime import date, timedelta, datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models

from members.models import Member
from attendance.models import Attendance
from subscriptions.models import Subscription
from gyms.models import Gym

from .models import Notification


# -------- Helper: safe notification creator --------
def create_notification(gym, member, notif_type, message):
    """Central place to create notifications (so duplicate logic na ho)."""
    return Notification.objects.create(
        gym=gym,
        member=member,
        notif_type=notif_type,
        message=message,
        is_read=False,
        is_sent=False,
    )


# -------- 1) Notification list page --------
def notifications_list(request):
    notif_type = request.GET.get("type", "all")

    notifications = (
        Notification.objects
        .select_related("member")
        .order_by("-sent_at")
    )

    if notif_type in ["expiry", "attendance", "general"]:
        notifications = notifications.filter(notif_type=notif_type)

    unread_count = Notification.objects.filter(is_read=False).count()

    context = {
        "notifications": notifications,
        "active_filter": notif_type,
        "unread_count": unread_count,
    }
    return render(request, "notifications/list.html", context)

# ==========================
# 2) MARK SINGLE AS READ
# ==========================
def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.is_read = True
    notif.save()
    messages.success(request, "Notification marked as read.")
    return redirect("notifications_list")

# ==========================
# 3) MARK ALL AS READ
# ==========================
def mark_all_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect("notifications_list")

# ==========================
# 4) DELETE NOTIFICATION
# ==========================
def delete_notification(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.delete()
    messages.success(request, "Notification deleted.")
    return redirect("notifications_list")

# ==========================
# 5) AUTO: EXPIRY REMINDERS
# ==========================
def send_expiry_reminders(request):
    today = date.today()
    upcoming = today + timedelta(days=3)

    expiring_soon = Subscription.objects.filter(
        end_date__lte=upcoming,
        end_date__gte=today,
    )

    gym = Gym.objects.first()

    created = 0
    for s in expiring_soon:
        msg = (
            f"Hi {s.member.full_name}, your plan '{s.plan.name}' "
            f"is expiring on {s.end_date}. Please renew soon."
        )

        Notification.objects.create(
            gym=gym,
            member=s.member,
            title="Membership Expiry Reminder",
            message=msg,
            notif_type="expiry",
            is_sent=False,
        )
        created += 1

    messages.success(request, f"Generated {created} expiry reminders.")
    return redirect("notifications_list")



# ==========================
# 6) AUTO: LOW ATTENDANCE SCAN
# ==========================
def scan_low_attendance(request):
    today = date.today()
    last_30 = today - timedelta(days=30)

    gym = Gym.objects.first()

    # Members with low attendance (0–3 punches in last 30 days)
    low_members = (
        Attendance.objects.filter(date__gte=last_30)
        .values("member_id")
        .annotate(cnt=models.Count("id"))
        .filter(cnt__lte=3)
    )

    member_ids = [row["member_id"] for row in low_members]

    members = Member.objects.filter(id__in=member_ids)

    created = 0
    for m in members:
        msg = (
            f"Hi {m.full_name}, we noticed you’ve visited less in the last month. "
            "Let’s get you back on track! 💪"
        )

        Notification.objects.create(
            gym=gym,
            member=m,
            title="We miss you at the gym",
            message=msg,
            notif_type="attendance",
            is_sent=False,
        )
        created += 1

    messages.success(request, f"Generated {created} low-attendance alerts.")
    return redirect("notifications_list")