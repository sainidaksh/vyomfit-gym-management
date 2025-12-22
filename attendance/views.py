from django.shortcuts import render, redirect
from datetime import date, timedelta
from django.db.models import Count
from django.contrib import messages

from .models import Attendance
from members.models import Member
from gyms.models import Gym


# ------------------------------
# TODAY ATTENDANCE LIST
# ------------------------------
def attendance_list(request):
    today = date.today()
    records = Attendance.objects.filter(date=today).select_related("member")
    return render(request, "attendance/list.html", {
        "records": records,
        "today": today
    })


# ------------------------------
# MARK PAGE (FORM + LIST)
# ------------------------------
def mark_attendance_page(request):
    members = Member.objects.all()
    gym = Gym.objects.first()

    if request.method == "POST":
        member_id = request.POST.get("member_id")

        # Already marked today?
        already = Attendance.objects.filter(
            member_id=member_id,
            date=date.today()
        ).exists()

        if already:
            messages.warning(request, "Attendance already marked for this member today.")
            return redirect("attendance_list")

        Attendance.objects.create(
            gym=gym,
            member_id=member_id,
            date=date.today()
        )

        messages.success(request, "Attendance marked successfully.")
        return redirect("attendance_list")

    return render(request, "attendance/mark_page.html", {
        "members": members,
        "today": date.today()
    })


# ------------------------------
# ONE TAP QUICK MARK BUTTON
# ------------------------------
def mark_attendance(request, member_id):
    gym = Gym.objects.first()

    # Already marked today?
    already = Attendance.objects.filter(
        member_id=member_id,
        date=date.today()
    ).exists()

    if already:
        messages.warning(request, "Attendance already marked for this member today.")
        return redirect("attendance_list")

    Attendance.objects.create(
        gym=gym,
        member_id=member_id,
        date=date.today()
    )

    messages.success(request, "Attendance marked successfully.")
    return redirect("attendance_list")


# ------------------------------
# ATTENDANCE ANALYTICS
# ------------------------------
def attendance_analytics(request):
    today = date.today()
    last_30 = today - timedelta(days=30)

    qs = Attendance.objects.filter(date__gte=last_30)

    total_punches = qs.count()

    stats = (
        qs.values("member_id", "member__full_name")
          .annotate(visits=Count("id"))
          .order_by("-visits")
    )

    return render(request, "attendance/analytics.html", {
        "stats": stats,
        "total_punches": total_punches,
        "start": last_30,
        "end": today,
    })
