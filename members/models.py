from django.db import models
from gyms.models import Gym
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import uuid
from PIL import Image
import qrcode
import os
from django.utils.timezone import now
from django.db.models import Count


def member_photo_path(instance, filename):
    """Uploads photo inside a folder gym-wise"""
    return f"member_photos/gym_{instance.gym.id}/{instance.member_id}/{filename}"


def qr_code_path(instance, filename):
    """Save QR code inside gym folder"""
    return f"qr_codes/gym_{instance.gym.id}/{instance.member_id}.png"


class Member(models.Model):

    # ---------- BASIC ----------
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="members")

    full_name = models.CharField(max_length=150)

    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^[0-9]{7,15}$", "Phone must contain only digits")],
    )

    email = models.EmailField(blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        blank=True,
        null=True,
    )

    age = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(10), MaxValueValidator(90)],
    )

    address = models.TextField(blank=True, null=True)

    join_date = models.DateField(auto_now_add=True)

    profile_photo = models.ImageField(
        upload_to=member_photo_path,
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    # ---------- ADVANCED FEATURES ----------
    member_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True
    )

    qr_code = models.ImageField(
        upload_to=qr_code_path,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-id"]
        unique_together = ("gym", "phone")

    def __str__(self):
        return f"{self.full_name} ({self.member_id})"

    # -----------------------------------------------------------
    # ⭐ 1) AUTO-GENERATE CUSTOM MEMBER ID (e.g., GYM3-2025-00012)
    # -----------------------------------------------------------
    def generate_member_id(self):
        last_member = Member.objects.filter(gym=self.gym).order_by("id").last()

        next_num = 1
        if last_member and last_member.member_id:
            try:
                next_num = int(last_member.member_id.split("-")[-1]) + 1
            except:
                pass

        return f"GYM{self.gym.id}-{now().year}-{str(next_num).zfill(5)}"

    # -----------------------------------------------------------
    # ⭐ 2) AUTO-RESIZE PROFILE PHOTO (300x300)
    # -----------------------------------------------------------
    def resize_image(self):
        if self.profile_photo:
            img = Image.open(self.profile_photo.path)
            img = img.convert("RGB")
            img.thumbnail((300, 300))
            img.save(self.profile_photo.path, quality=85, optimize=True)

    # -----------------------------------------------------------
    # ⭐ 3) AUTO-GENERATE QR CODE for Attendance
    # -----------------------------------------------------------
    def generate_qr(self):
        qr_text = f"MEMBER:{self.member_id}"
        qr_img = qrcode.make(qr_text)

        path = f"media/qr_codes/gym_{self.gym.id}/"
        os.makedirs(path, exist_ok=True)

        file_path = os.path.join(path, f"{self.member_id}.png")
        qr_img.save(file_path)

        self.qr_code = f"qr_codes/gym_{self.gym.id}/{self.member_id}.png"

    # -----------------------------------------------------------
    # ⭐ SAVE OVERRIDE (Auto generate ID, QR & resize photo)
    # -----------------------------------------------------------
    def save(self, *args, **kwargs):

        # generate member ID if not exists
        if not self.member_id:
            self.member_id = self.generate_member_id()

        super().save(*args, **kwargs)

        # resize photo AFTER saving
        self.resize_image()

        # generate QR AFTER member_id exists
        if not self.qr_code:
            self.generate_qr()
            super().save(update_fields=["qr_code"])

    # -----------------------------------------------------------
    # ⭐ 4) Previous Subscription History
    # -----------------------------------------------------------
    @property
    def subscription_history(self):
        return self.subscription_set.order_by("-start_date")

    # -----------------------------------------------------------
    # ⭐ 5) Monthly Visit Count (Attendance Analytics)
    # -----------------------------------------------------------
    @property
    def monthly_visits(self):
        from attendance.models import Attendance

        return Attendance.objects.filter(
            member=self,
            date__month=now().month,
            date__year=now().year
        ).count()

    # Helper: check if any active subscription exists
    @property
    def has_active_subscription(self):
        return self.subscription_set.filter(status="active").exists()

    @property
    def first_name(self):
        return self.full_name.split()[0]
