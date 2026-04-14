from rest_framework import serializers

from hub.models import Execution, Rating, Task, User


class UserPublicSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(source="date_joined", read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "name", "created_at")
        read_only_fields = fields


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    name = serializers.CharField(max_length=120)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TaskSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "user_id",
            "title",
            "prompt_body",
            "description",
            "is_reusable",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user_id", "created_at", "updated_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class ExecutionSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.none(), source="task"
    )

    class Meta:
        model = Execution
        fields = (
            "id",
            "task_id",
            "user_id",
            "input_payload",
            "output_payload",
            "meta",
            "created_at",
        )
        read_only_fields = ("id", "user_id", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["task_id"].queryset = Task.objects.filter(user=request.user)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["task_id"] = instance.task_id
        return ret


class RatingSerializer(serializers.ModelSerializer):
    execution_id = serializers.PrimaryKeyRelatedField(
        queryset=Execution.objects.none(), source="execution"
    )

    class Meta:
        model = Rating
        fields = ("id", "user_id", "execution_id", "score", "comment", "created_at")
        read_only_fields = ("id", "user_id", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["execution_id"].queryset = Execution.objects.filter(
                user=request.user
            )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def validate_score(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Score must be 1-5")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        ex = attrs.get("execution")
        if ex and Rating.objects.filter(user=user, execution=ex).exists():
            raise serializers.ValidationError("Already rated this execution")
        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["execution_id"] = instance.execution_id
        return ret
