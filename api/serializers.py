# from rest_framework import serializers
# from .models import Client, Project
# from django.contrib.auth.models import User

# # 1. For listing user info
# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='username')

#     class Meta:
#         model = User
#         fields = ['id', 'name']


# # 2. For listing/creating clients
# class ClientSerializer(serializers.ModelSerializer):
#     created_by = serializers.ReadOnlyField(source='created_by.username')

#     class Meta:
#         model = Client
#         fields = ['id', 'client_name', 'created_by', 'created_at']

# # 3. For full project view
# class ProjectSerializer(serializers.ModelSerializer):
#     created_by = serializers.ReadOnlyField(source='created_by.username')
#     client = serializers.CharField(source='client.client_name', read_only=True)
#     users = serializers.SerializerMethodField()

#     class Meta:
#         model = Project
#         fields = ['id', 'project_name', 'client', 'users', 'created_by', 'created_at']

#     def get_users(self, obj):
#         return [
#             {
#                 'id': user.id,
#                 'name': user.username
#             }
#             for user in obj.users.all()
#         ]



# # 4. For creating a project (assigning users)
# # api/serializers.py

# class ProjectCreateSerializer(serializers.ModelSerializer):
#     users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
#     client = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Project
#         fields = ['id', 'project_name', 'client', 'users', 'created_by', 'created_at']
#         read_only_fields = ['created_by', 'created_at']



# # 5. For detailed client view with their projects
# class ClientDetailSerializer(serializers.ModelSerializer):
#     projects = ProjectSerializer(many=True, read_only=True)
#     created_by = serializers.ReadOnlyField(source='created_by.username')

#     class Meta:
#         model = Client
#         fields = ['id', 'client_name', 'created_by', 'created_at', 'projects']



from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User


# 1. User Serializer
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ['id', 'name']

# 2. Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_by', 'created_at']

# 3. Project Serializer (for viewing full project info)
class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    clients = ClientSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'clients', 'users', 'created_by', 'created_at']

# 4. Project Create Serializer (for POST)
class ProjectCreateSerializer(serializers.ModelSerializer):
    clients = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), many=True)
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'clients', 'users', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def create(self, validated_data):
        users = validated_data.pop('users')
        clients = validated_data.pop('clients')
        project = Project.objects.create(**validated_data)
        project.users.set(users)
        project.clients.set(clients)
        return project

# 5. Client Detail Serializer
class ClientDetailSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_by', 'created_at', 'projects']
