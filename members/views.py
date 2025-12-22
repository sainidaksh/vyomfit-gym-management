from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now

from .models import Member
from gyms.models import Gym
from subscriptions.models import Subscription
from attendance.models import Attendance
from payments.models import Payment


# =========================================================
#   ADD MEMBER (Secure + Validated + Multi-GYM Ready)
# =========================================================
def add_member(request):
    gym = request.user.gym if hasattr(request.user, "gym") else Gym.objects.first()

    if request.method == 'POST':
        name = request.POST.get('full_name').strip()
        phone = request.POST.get('phone').strip()
        gender = request.POST.get('gender')
        age = request.POST.get('age') or None
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Duplicate phone check inside SAME GYM
        if Member.objects.filter(gym=gym, phone=phone).exists():
            messages.error(request, "This phone number already exists in your gym.")
            return redirect("add_member")

        member = Member.objects.create(
            gym=gym,
            full_name=name,
            phone=phone,
            gender=gender,
            age=age,
            email=email,
            address=address
        )

        messages.success(request, f"Member {member.full_name} added successfully!")
        return redirect("members_list")

    return render(request, "members/add_member.html")


# =========================================================
#   MEMBERS LIST (Gym-wise filtering + search)
# =========================================================
def members_list(request):
    gym = request.user.gym if hasattr(request.user, "gym") else Gym.objects.first()

    members = Member.objects.filter(gym=gym).order_by("-id")

    query = request.GET.get("q")
    if query:
        members = members.filter(full_name__icontains=query)

    context = {
        "members": members,
        "total_members": members.count(),
    }
    return render(request, "members/list.html", context)


# =========================================================
#   DELETE MEMBER (Safe Delete)
# =========================================================
def member_delete(request, id):
    gym = request.user.gym if hasattr(request.user, "gym") else Gym.objects.first()

    member = get_object_or_404(Member, id=id, gym=gym)
    member.delete()

    messages.success(request, "Member deleted successfully.")
    return redirect("members_list")


# =========================================================
#   EDIT MEMBER (Safety + Validation + Gym Isolation)
# =========================================================
def member_edit(request, id):
    gym = request.user.gym if hasattr(request.user, "gym") else Gym.objects.first()

    member = get_object_or_404(Member, id=id, gym=gym)

    if request.method == "POST":
        full_name = request.POST.get("full_name").strip()
        phone = request.POST.get("phone").strip()
        gender = request.POST.get("gender")
        age = request.POST.get("age") or None
        email = request.POST.get("email")
        address = request.POST.get("address")

        # Check duplicate phone for other members in same gym
        if Member.objects.filter(gym=gym, phone=phone).exclude(id=member.id).exists():
            messages.error(request, "Another member with this phone already exists.")
            return redirect("member_edit", id=member.id)

        member.full_name = full_name
        member.phone = phone
        member.gender = gender
        member.age = age
        member.email = email
        member.address = address
        member.save()

        messages.success(request, "Member details updated.")
        return redirect("members_list")

    return render(request, "members/edit_member.html", {"member": member})


# =========================================================
#   MEMBER DETAIL PAGE (Full Analytics + History)
# =========================================================
def member_detail(request, id):
    gym = request.user.gym if hasattr(request.user, "gym") else Gym.objects.first()

    member = get_object_or_404(Member, id=id, gym=gym)

    # Subscription History
    subs = member.subscription_history  # (from model property)
    active_sub = subs.filter(status="active").first()
    last_sub = subs.first()

    # Attendance stats
    today = now().date()
    month_start = today.replace(day=1)

    total_visits = Attendance.objects.filter(member=member).count()
    month_visits = member.monthly_visits  # (from model property)
    last_visit = Attendance.objects.filter(member=member).order_by('-date', '-time').first()

    # Payments
    payments = Payment.objects.filter(subscription__member=member).order_by("-payment_date")
    total_paid = payments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        "member": member,
        "subscriptions": subs,
        "active_sub": active_sub,
        "last_sub": last_sub,
        "total_visits": total_visits,
        "month_visits": month_visits,
        "last_visit": last_visit,
        "payments": payments,
        "total_paid": total_paid,
    }

    return render(request, "members/detail.html", context)
