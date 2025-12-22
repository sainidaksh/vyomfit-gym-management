from django.db import models
from subscriptions.models import Subscription
from notifications.models import Notification   # ⭐ ADD THIS IMPORT


class Payment(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_date = models.DateTimeField(auto_now_add=True)

    PAYMENT_MODES = (
        ("cash", "Cash"),
        ("online", "Online"),
        ("upi", "UPI"),
        ("card", "Card"),
    )
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODES)

    def __str__(self):
        return f"{self.subscription.member.full_name} - ₹{self.amount}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # नया payment होने पर notification बनाओ
        if is_new:
            sub = self.subscription
            msg = f"Payment received: ₹{self.amount} for plan {sub.plan.name}."

            Notification.objects.create(
                gym=sub.gym,
                member=sub.member,
                notif_type="payment",
                message=msg,
                is_sent=False
            )
