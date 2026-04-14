from math import ceil

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from hub.models import Execution, Rating, Task
from hub.response import err, ok
from hub.serializers import (
    ExecutionSerializer,
    LoginSerializer,
    RatingSerializer,
    RegisterSerializer,
    TaskSerializer,
    UserPublicSerializer,
)

User = get_user_model()


def _tokens_for(user):
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)
    return {"access_token": str(refresh.access_token), "token_type": "Bearer"}


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].lower()
        if User.objects.filter(email=email).exists():
            return err("Email already registered", 400, "Email already registered", 400)
        user = User.objects.create_user(
            email=email,
            password=ser.validated_data["password"],
            name=ser.validated_data["name"],
        )
        return ok(
            {"user": UserPublicSerializer(user).data, "tokens": _tokens_for(user)},
            "Created",
            status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].lower()
        password = ser.validated_data["password"]
        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return err("Invalid credentials", 401, None, 401)
        return ok({"user": UserPublicSerializer(user).data, "tokens": _tokens_for(user)})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ok(UserPublicSerializer(request.user).data)


class TaskCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = max(1, int(request.query_params.get("page", 1)))
        per_page = min(100, max(1, int(request.query_params.get("per_page", 20))))
        qs = Task.objects.filter(user=request.user).order_by("-created_at")
        total = qs.count()
        items = qs[(page - 1) * per_page : page * per_page]
        data = {
            "items": TaskSerializer(items, many=True).data,
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": max(1, ceil(total / per_page)) if per_page else 1,
        }
        return ok(data)

    def post(self, request):
        ser = TaskSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        t = ser.save()
        return ok(TaskSerializer(t).data, "Created", status.HTTP_201_CREATED)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return Task.objects.filter(pk=pk, user=request.user).first()

    def get(self, request, pk):
        t = self.get_object(request, pk)
        if not t:
            return err("Not found", 404, None, 404)
        return ok(TaskSerializer(t).data)

    def put(self, request, pk):
        t = self.get_object(request, pk)
        if not t:
            return err("Not found", 404, None, 404)
        ser = TaskSerializer(t, data=request.data, context={"request": request}, partial=False)
        ser.is_valid(raise_exception=True)
        ser.save()
        return ok(TaskSerializer(t).data)

    def delete(self, request, pk):
        t = self.get_object(request, pk)
        if not t:
            return err("Not found", 404, None, 404)
        t.delete()
        return ok(None, "Deleted")


class ExecutionCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        task_id = request.query_params.get("task_id")
        qs = Execution.objects.filter(user=request.user)
        if task_id is not None:
            qs = qs.filter(task_id=int(task_id))
        qs = qs.order_by("-created_at")
        return ok({"items": ExecutionSerializer(qs, many=True).data})

    def post(self, request):
        ser = ExecutionSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        e = ser.save()
        return ok(ExecutionSerializer(e).data, "Created", status.HTTP_201_CREATED)


class RatingCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ex_id = request.query_params.get("execution_id")
        qs = Rating.objects.filter(user=request.user)
        if ex_id is not None:
            qs = qs.filter(execution_id=int(ex_id))
        qs = qs.order_by("-created_at")
        return ok({"items": RatingSerializer(qs, many=True).data})

    def post(self, request):
        ser = RatingSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        r = ser.save()
        return ok(RatingSerializer(r).data, "Created", status.HTTP_201_CREATED)
