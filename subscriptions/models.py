from datetime import date, timedelta
from django.db import models
from gyms.models import Gym
from members.models import Member
from plans.models import Plan

class Subscription(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='active')

    def save(self, *args, **kwargs):
        # Auto-calc expiry if end_date missing
        if not self.end_date:
            if self.plan.duration_type == "days":
                self.end_date = self.start_date + timedelta(days=self.plan.duration_value)

            elif self.plan.duration_type == "weeks":
                self.end_date = self.start_date + timedelta(weeks=self.plan.duration_value)

            elif self.plan.duration_type == "months":
                # months = 30 days (simple approach) or use relativedelta
                from dateutil.relativedelta import relativedelta
                self.end_date = self.start_date + relativedelta(months=self.plan.duration_value)

        # Update STATUS
        if self.end_date < date.today():
            self.status = "expired"
        else:
            self.status = "active"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.full_name} - {self.plan.name}"
