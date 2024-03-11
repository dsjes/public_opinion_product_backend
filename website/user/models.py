from django.db import models
from django.contrib.auth.hashers import make_password


class Plan(models.Model):
    plan_choices = [("0", "尚未付款"), ("1", "1人方案"), ("2", "5人方案"), ("3", "20人方案")]
    plan = models.CharField(choices=plan_choices, null=False, max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "plans"


class Member(models.Model):
    uid = models.CharField(max_length=128, unique=True, null=False)  # 企業統編
    uuid = models.CharField(
        max_length=128, unique=True, null=False
    )  # 生成一組亂碼用來放在 jwt 裡面
    name = models.CharField(max_length=50, null=False)
    plan = models.ForeignKey(
        Plan, null=False, on_delete=models.CASCADE, related_name="member_plan"
    )
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = "members"


class ClientUser(models.Model):
    permission_choices = [(0, "admin"), (1, "editor"), (2, "viewer")]

    name = models.CharField(max_length=50, unique=True, null=False)
    line_user_id = models.CharField(max_length=50, unique=True, blank=True)
    email = models.CharField(max_length=50, unique=True, null=False)
    phone = models.CharField(max_length=50, unique=True, null=False)
    line_token = models.CharField(max_length=50, unique=True)
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="client_users"
    )
    displayable = models.BooleanField(
        default=True, null=False
    )  # 顯示在使用者管理頁面的條件:預設負責人新增完使用者就會顯示在頁面上
    enabled = models.BooleanField(default=False, null=False)  # 服務開通，刪除使用者時要關掉權限
    permission = models.IntegerField(choices=permission_choices, null=False)
    is_contact = models.BooleanField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"


class HashUserPassword(models.Model):
    user_id = models.ForeignKey(ClientUser, on_delete=models.CASCADE, null=False)
    hashed_password = models.CharField(max_length=100, null=False)
    only_once = models.BooleanField(
        default=False, null=False
    )  # for 忘記密碼時，生成臨時密碼使用，臨時密碼只能使用一次
    enabled = models.BooleanField(default=True, null=False)  # 忘記密碼或是更改密碼時，要改掉
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hash_user_passwords"
