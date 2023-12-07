from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(verbose_name="별명", max_length=16, null=False)
    password = models.CharField(verbose_name="패스워드", max_length=20)
    phone_number = models.CharField(max_length=15, null=True)
    register_date = models.DateTimeField(auto_now_add=True, null=False)
    profile_number = models.IntegerField(default=1)
    personal_consent = models.BooleanField(default=False)

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return str(self.id)


class UserDevice(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="", null=True
    )
    fcm_token = models.CharField("FCM Token", blank=True, max_length=500, null=True)

    class Meta:
        db_table = 'User_Device'


class UserAlarm(models.Model):
    register_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True),
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True),
    alarm_message = models.CharField(max_length=100, null=False),
    content_type = models.IntegerField(null=False, blank=False),
    content_id = models.IntegerField(null=True, blank=True),
    register_date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = 'User_Alarm'

    def create_user_alarm(register_user, target_user, content_type, content_id):
        alarm_message = ""
        if content_type == 1:
            alarm_message = "당신의 실종 동물에 대한 제보가 들어왔습니다."
        if content_type == 2:
            alarm_message = "누군가가 동물을 잃어버렸습니다."
        if content_type == 3:
            alarm_message = "당신의 게시글에 발자국을 남겼습니다."

        user_alarm = UserAlarm.objects.create(
            register_user=register_user,
            target_user=target_user,
            alarm_message=alarm_message,
            content_type=content_type,
            content_id=content_id,
        )

        return user_alarm

    def __str__(self):
        return str(self.id)
