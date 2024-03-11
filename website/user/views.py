from user.serializer import ClientSerializer, MemberSerializer, HashedPasswordSerializer
from user.models import ClientUser, Member, Plan, HashUserPassword
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


error_messages = {"0": "正確", "1": "統一編號須為 8 碼", "2": "Email 格式錯誤", "3": "電話格式錯誤"}


# 負責人註冊時會直接創建 member 與 user(負責人) 身分
class MemberSignUpView(APIView):
    # TODO:生成 UUID 與 Line Token
    # authentication_classes = [IsAuthenticated]

    def validate_data(self, request):
        uid_data = request.data.get("uid")
        email_data = request.data.get("email")
        phone_data = request.data.get("phone")
        if len(uid_data) != 8:
            return False, error_messages["1"]
        if "@" not in str(email_data) or "." not in str(email_data):
            return False, error_messages["2"]
        if len(phone_data) != 10 or str(phone_data)[:1] == "09":
            return False, error_messages["3"]
        return True, error_messages["0"]

    def collect_member_data(self, request):
        plan = Plan.objects.get(pk=2)
        data = {
            "name": request.data.get("name"),
            "uid": request.data.get("uid"),
            "uuid": request.data.get("uuid"),
            "plan": plan.id,
        }
        return data

    def collect_client_data(self, request):
        db_member = Member.objects.filter(name=request.data.get("name")).first()
        if db_member is None:
            return Response("沒有該會員資料", status=status.HTTP_204_NO_CONTENT)
        print(db_member)

        data = {
            "name": request.data.get("client_name"),
            "email": request.data.get("email"),
            "phone": request.data.get("phone"),
            "permission": 0,
            "is_contact": True,
            "member": db_member.id,
            "line_token": str(uuid.uuid4()),
        }
        return data

    def get(self, request):
        db_members = Member.objects.all()
        serializer = MemberSerializer(db_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print("request.data", request.data)
        result, error_message = self.validate_data(request)
        if not result:
            return Response(data=error_message, status=status.HTTP_400_BAD_REQUEST)

        member_data = self.collect_member_data(request)
        print("member data", member_data)
        member_serializer = MemberSerializer(data=member_data)
        if not member_serializer.is_valid():
            return Response(
                member_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        member_serializer.save()
        print("Member data saved successfully!")

        client_data = self.collect_client_data(request)
        print("client data", client_data)
        client_serializer = ClientSerializer(data=client_data)
        if not client_serializer.is_valid():
            return Response(
                client_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        client_serializer.save()
        print("client data saved successfully!")

        return Response(
            "member and contact data have been created successfully",
            status=status.HTTP_201_CREATED,
        )


# 新使用者註冊
class ClientSingUpView(APIView):
    # authentication_classes = [IsAuthenticated]

    def get(self, request):
        db_users = ClientUser.objects.all()
        serializer = ClientSerializer(db_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_email_valid(self, request):
        print("checking email...")
        email = request.data.get("email")
        print("email", email)
        db_user = ClientUser.objects.filter(email=email).first()
        if db_user:
            print("email check pass")
            return True, db_user.id

        return False, None

    def hash_password(self, request):
        password = request.data.get("password")
        hashed_password = make_password(password)
        print("hash password successfully")
        return hashed_password

    def generate_line_token(self):
        line_token = str(uuid.uuid4())
        return line_token

    def update_client_data(self, user_id):
        db_user = ClientUser.objects.filter(id=user_id).first()
        db_user.update(line_token=self.generate_line_token())
        print("line token updated successfully")

    def post(self, request):
        email_valid, user_id = self.check_email_valid(request)
        if email_valid:
            hashed_password = self.hash_password(request)

            data = {"user_id": user_id, "hashed_password": hashed_password}
            hash_password_serializer = HashedPasswordSerializer(data=data)
            if hash_password_serializer.is_valid():
                hash_password_serializer.save()
                print("hashed password save successfully")
                return Response(
                    "client data has been created.", status=status.HTTP_201_CREATED
                )
            self.update_client_data()
            return Response(
                hash_password_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response("email isn't valid", status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            db_user = ClientUser.objects.filter(email=email).first()
            hashed_password = HashUserPassword.objects.get(
                user_id=db_user.id
            ).hashed_password
        except Exception as e:
            return Response(
                e,
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, hashed_password):
            return Response(
                {"error": "invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(db_user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
