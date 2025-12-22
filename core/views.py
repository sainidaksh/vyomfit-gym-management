# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta

from members.models import Member
from subscriptions.models import Subscription
from attendance.models import Attendance
from payments.models import Payment


# =====================================================================
# 🔵 MAIN DASHBOARD
# =====================================================================
@login_required
def dashboard(request):

    today = timezone.localdate()
    last_30 = today - timedelta(days=30)

    total_members = Member.objects.count()
    active_subscriptions = Subscription.objects.filter(status='active').count()
    expired_subscriptions = Subscription.objects.filter(status='expired').count()
    today_attendance = Attendance.objects.filter(date=today).count()

    visit_data = (
        Attendance.objects.filter(date__gte=last_30)
        .values('member')
        .annotate(visits=Count('id'))
    )

    visit_map = {row["member"]: row["visits"] for row in visit_data}

    high_engaged = regular_members = low_attendance = 0

    for visits in visit_map.values():
        if visits >= 16:
            high_engaged += 1
        elif visits >= 9:
            regular_members += 1
        elif visits >= 4:
            low_attendance += 1

    counted_members = high_engaged + regular_members + low_attendance
    at_risk_members = max(total_members - counted_members, 0)

    context = {
        "total_members": total_members,
        "active_subscriptions": active_subscriptions,
        "expired_subscriptions": expired_subscriptions,
        "today_attendance": today_attendance,

        "high_engaged": high_engaged,
        "regular_members": regular_members,
        "low_attendance": low_attendance,
        "at_risk_members": at_risk_members,
    }

    return render(request, "dashboard.html", context)


# =====================================================================
# 🔵 LOGOUT
# =====================================================================
def logout_page(request):
    return render(request, "logout.html")


def logout_confirm(request):
    logout(request)
    return redirect("/login/")


# =====================================================================
# 🔵 ADVANCED ANALYTICS PAGE
# =====================================================================
@login_required
def analytics_view(request):

    today = timezone.localdate()
    six_months_ago = today - timedelta(days=180)

    total_members = Member.objects.count()
    active_subscriptions = Subscription.objects.filter(status="active").count()
    expired_subscriptions = Subscription.objects.filter(status="expired").count()
    today_attendance = Attendance.objects.filter(date=today).count()

    total_revenue = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0

    # ---- REVENUE CHART ----
    revenue = (
        Payment.objects.filter(payment_date__date__gte=six_months_ago)
        .annotate(month=TruncMonth("payment_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    revenue_labels = [r["month"].strftime("%Y-%m") for r in revenue]
    revenue_values = [float(r["total"]) for r in revenue]

    # ---- MEMBER GROWTH ----
    member_growth = (
        Member.objects.filter(join_date__gte=six_months_ago)
        .annotate(month=TruncMonth("join_date"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    members_labels = [m["month"].strftime("%Y-%m") for m in member_growth]
    members_values = [m["count"] for m in member_growth]

    context = {
        "total_members": total_members,
        "active_subscriptions": active_subscriptions,
        "expired_subscriptions": expired_subscriptions,
        "today_attendance": today_attendance,

        "total_revenue": total_revenue,

        "revenue_labels": revenue_labels,
        "revenue_values": revenue_values,

        "members_labels": members_labels,
        "members_values": members_values,
    }

    return render(request, "analytics.html", context)
