from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class Course(models.Model):
    department = models.CharField(max_length=16, help_text="Department string, like COMPSCI or MATH.")
    number = models.IntegerField(
        validators=[
            validators.MinValueValidator(100),
            validators.MaxValueValidator(999),
        ],
        help_text="Course number, like the 187 in COMPSCI 187.",
    )
    name = models.CharField(
        max_length=64,
        help_text='The human-legible name of the course, like "Programming with Data Structures."',
    )

    def __str__(self):
        return f"{self.department} {self.number}: {self.name}"


class LRCDatabaseUser(AbstractUser):
    courses_tutored = models.ManyToManyField(Course)

    def __str__(self):
        if not (self.first_name and self.last_name):
            return self.username
        else:
            return f"{self.first_name} {self.last_name}"


class TutoringShift(models.Model):
    tutor = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        help_text="The tutor who is responsible for this session.",
    )
    start = models.DateTimeField(help_text="The time that the session starts.")
    duration = models.DurationField(help_text="How long the session will last, in HH:MM:SS format.")
    location = models.CharField(
        max_length=32,
        help_text="The location where the session will be held, e.g. GSMN 64.",
    )

    def __str__(self):
        return f"{self.tutor} in {self.location} at {self.start}"


class TutoringShiftChangeRequest(models.Model):
    target = models.ForeignKey(
        to=TutoringShift,
        related_name="tutoring_shift_change_request_target",
        on_delete=models.CASCADE,
        help_text="Tutoring shift to edit.",
    )
    reason = models.CharField(max_length=512, help_text="Explanation for why this change is being requested.")
    approved = models.BooleanField(default=False, help_text="Whether the request is approved or not.")
    approved_by = models.ForeignKey(
        to=LRCDatabaseUser,
        related_name="tutoring_shift_change_request_approved_by",
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        help_text="The user (if any) who approved the change request.",
    )
    approved_on = models.DateTimeField(help_text="When the request was approved.", blank=True, null=True, default=None)

    new_tutor = models.ForeignKey(
        to=LRCDatabaseUser,
        related_name="tutoring_shift_change_request_new_tutor",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        help_text="The new tutor who will be responsible for the session if this request is approved.",
    )
    new_start = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="The new time that the session starts if this request is approved.",
    )
    new_duration = models.DurationField(
        blank=True,
        null=True,
        default=None,
        help_text="How long the session will last, in HH:MM:SS format, if this request is approved.",
    )
    new_location = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        default=None,
        help_text="The new location where this session will be held, e.g. GSMN 64, if this request is approved.",
    )


class SISession(models.Model):
    class Meta:
        verbose_name = "SI session"
        verbose_name_plural = "SI sessions"

    si_leader = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        help_text="The SI leader who is responsible for this session.",
    )
    start = models.DateTimeField(help_text="The time that the session starts.")
    duration = models.DurationField(help_text="How long the session will last, in HH:MM:SS format.")
    location = models.CharField(
        max_length=32,
        help_text="The location where the session will be held, e.g. GSMN 64.",
    )

    def __str__(self):
        return f"{self.si_leader} in {self.location} at {self.start}"


class SISessionChangeRequest(models.Model):
    class Meta:
        verbose_name = "SI session change request"
        verbose_name_plural = "SI session change requests"

    target = models.ForeignKey(
        to=SISession,
        related_name="si_session_change_request_target",
        on_delete=models.CASCADE,
        help_text="SI session to edit.",
    )
    reason = models.CharField(max_length=512, help_text="Explanation for why this change is being requested.")
    approved = models.BooleanField(default=False, help_text="Whether the request is approved or not.")
    approved_by = models.ForeignKey(
        to=LRCDatabaseUser,
        related_name="si_session_change_request_approved_by",
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        help_text="The user (if any) who approved the change request.",
    )
    approved_on = models.DateTimeField(help_text="When the request was approved.", blank=True, null=True, default=None)

    new_si_leader = models.ForeignKey(
        to=LRCDatabaseUser,
        related_name="si_session_change_request_new_si_leader",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        help_text="The new SI leader who will be responsible for the session if this request is approved.",
    )
    new_start = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="The new time that the session starts if this request is approved.",
    )
    new_duration = models.DurationField(
        blank=True,
        null=True,
        default=None,
        help_text="How long the session will last, in HH:MM:SS format, if this request is approved.",
    )
    new_location = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        default=None,
        help_text="The new location where this session will be held, e.g. GSMN 64, if this request is approved.",
    )


class Hardware(models.Model):
    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    target = models.ForeignKey(
        to=Hardware,
        related_name="intended_hardware_to_borrow",
        on_delete=models.CASCADE,
        help_text="The desired hardware being requested   ",
    )

    hardware_user = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        help_text="  The LRC user borrowing the hardware",
    )

    start_time = models.DateTimeField()

    return_time = models.DateTimeField(null=True, blank=True)
