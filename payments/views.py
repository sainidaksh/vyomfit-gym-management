from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from subscriptions.models import Subscription


from django.db.models import Sum
from datetime import date

def payment_list(request):
    payments = Payment.objects.all().order_by("-payment_date")

    today = date.today()
    first_day = today.replace(day=1)

    revenue_today = Payment.objects.filter(
    payment_date__date=today
).aggregate(Sum("amount"))["amount__sum"] or 0

    revenue_month = Payment.objects.filter(payment_date__gte=first_day).aggregate(Sum("amount"))["amount__sum"] or 0
    revenue_total = Payment.objects.aggregate(Sum("amount"))["amount__sum"] or 0

    return render(request, "payments/list.html", {
        "payments": payments,
        "revenue_today": revenue_today,
        "revenue_month": revenue_month,
        "revenue_total": revenue_total,
    })



# ⭐ 2 — Add Payment
def payment_add(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)

    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        mode = request.POST.get("payment_mode")

        Payment.objects.create(
            subscription=subscription,
            amount=amount,
            payment_mode=mode,
            payment_date=date.today(),   # FIX 1
            status="success"             # FIX 2 (if status exists)
        )

        return redirect("payment_list")

    return render(request, "payments/add.html", {
        "subscription": subscription
    })
