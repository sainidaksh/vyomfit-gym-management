from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta, datetime
from .models import Subscription
from members.models import Member
from plans.models import Plan
from gyms.models import Gym
from payments.models import Payment

# ⭐ 1 — Subscription List
def subscriptions_list(request):
    subscriptions = Subscription.objects.select_related('member', 'plan').all()
    return render(request, 'subscriptions/list.html', {"subscriptions": subscriptions})


# ⭐ 2 — Add Subscription + Auto Payment + Undo
def add_subscription(request):
    members = Member.objects.all()
    plans = Plan.objects.all()

    if request.method == 'POST':
        member_id = request.POST.get('member')
        plan_id = request.POST.get('plan')

        member = Member.objects.get(id=member_id)
        plan = Plan.objects.get(id=plan_id)
        gym = Gym.objects.first()

        start = date.today()

        # ⭐ NEW FLEXI DURATION SYSTEM
        if plan.duration_type == "days":
            end = start + timedelta(days=plan.duration_value)

        elif plan.duration_type == "weeks":
            end = start + timedelta(weeks=plan.duration_value)

        elif plan.duration_type == "months":
            end = start + timedelta(days=plan.duration_value * 30)

        else:
            end = start  # fallback

        # ⭐ Create Subscription
        new_sub = Subscription.objects.create(
            gym=gym,
            member=member,
            plan=plan,
            start_date=start,
            end_date=end,
            status="active"
        )

        # ⭐ Auto Payment Entry
        Payment.objects.create(
            subscription=new_sub,
            amount=plan.price,
            payment_mode="cash"
        )

        # ⭐ Store undo action
        request.session["last_action"] = {
            "type": "add",
            "subscription_id": new_sub.id
        }

        return redirect("subscriptions_list")

    return render(request, "subscriptions/add.html", {
        "members": members,
        "plans": plans,
    })


def payments_list(request):
    payments = Payment.objects.select_related('subscription', 'subscription__member')
    return render(request, 'subscriptions/payments.html', {'payments': payments})



# ⭐ 3 — Refresh Expiry (THIS WAS MISSING — NOW FIXED!!!)
def refresh_expiry(request):
    today = date.today()

    for sub in Subscription.objects.all():
        sub.status = "expired" if sub.end_date < today else "active"
        sub.save()

    return redirect("subscriptions_list")


# ⭐ 4 — Renew Subscription + Undo
def renew_subscription(request, id):
    
    sub = get_object_or_404(Subscription, id=id)

    if request.method == "POST":
        amount = request.POST.get("amount")
        mode = request.POST.get("payment_mode")

        # Undo info store
        request.session["last_action"] = {
            "type": "renew",
            "subscription_id": sub.id,
            "old_start": str(sub.start_date),
            "old_end": str(sub.end_date),
        }

        # Duration calculate
        if sub.plan.duration_type == "months":
            days = sub.plan.duration_value * 30
        elif sub.plan.duration_type == "weeks":
            days = sub.plan.duration_value * 7
        else:
            days = sub.plan.duration_value

        new_start = sub.end_date + timedelta(days=1)
        new_end = new_start + timedelta(days=days)

        sub.start_date = new_start
        sub.end_date = new_end
        sub.status = "active"
        sub.save()

        Payment.objects.create(
            subscription=sub,
            amount=amount,
            payment_mode=mode
        )

        return redirect("subscriptions_list")

    # GET request → show renew form page
    return render(request, "subscriptions/renew.html", {"sub": sub})


# ⭐ 5 — Delete Subscription + Undo
def subscription_delete(request, id):
    sub = get_object_or_404(Subscription, id=id)

    request.session["last_action"] = {
        "type": "delete",
        "subscription_id": sub.id,
        "member_id": sub.member_id,
        "plan_id": sub.plan_id,
        "gym_id": sub.gym_id,
        "start_date": str(sub.start_date),
        "end_date": str(sub.end_date),
        "status": sub.status
    }

    sub.delete()

    return redirect("subscriptions_list")


# ⭐ 6 — Undo Action (Supports Delete)
def undo_action(request):
    action = request.session.get('last_action')

    if not action:
        return redirect('subscriptions_list')

    if action["type"] == "delete":
        start = datetime.strptime(action["start_date"], '%Y-%m-%d').date()
        end = datetime.strptime(action["end_date"], '%Y-%m-%d').date()

        Subscription.objects.create(
            id=action["subscription_id"],
            member_id=action["member_id"],
            plan_id=action["plan_id"],
            gym_id=action["gym_id"],
            start_date=start,
            end_date=end,
            status=action["status"]
        )

    elif action["type"] == "renew":
        sub = Subscription.objects.get(id=action["subscription_id"])
        sub.start_date = datetime.strptime(action["old_start"], '%Y-%m-%d').date()
        sub.end_date = datetime.strptime(action["old_end"], '%Y-%m-%d').date()
        sub.save()

    # ⭐ Clear undo
    request.session.pop('last_action', None)

    return redirect('subscriptions_list')
