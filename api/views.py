from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import Client, Project
from .serializers import (
    ClientSerializer,
    ClientDetailSerializer,
    ProjectSerializer,
    ProjectCreateSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User

# ================================
# HTML Views (optional)
# ================================

def home_view(request):
    return render(request, 'home.html')

@login_required
def client_list_view(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

@login_required
def create_client_form(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        Client.objects.create(
            client_name=client_name,
            created_by=request.user,
            created_at=timezone.now()
        )
        return render(request, 'create_client.html', {'message': 'Client created successfully!'})
    return render(request, 'create_client.html')


# ================================
# REST API Views
# ================================

# 1. Create/List Clients
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# 2. Retrieve/Edit/Delete a Single Client
class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientDetailSerializer  # With project details
        return ClientSerializer  # For PUT/PATCH

# 3. Create Project for one or more clients and users
class ProjectCreateView(generics.CreateAPIView):         #Not Understand
    serializer_class = ProjectCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        self.project = project  # store to return full project data

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        output_serializer = ProjectSerializer(self.project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

# 4. View Projects Assigned to Logged-In User
# class UserProjectsView(generics.ListAPIView):
#     serializer_class = ProjectSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Project.objects.filter(users=self.request.user)

# 5. List All Users (for assigning to project)
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# 6. List All Clients (extra)
class ClientListAPIView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


# 7. Retrieve/Update a single project :  (Its showing only user and client only id)
# class ProjectDetailView(generics.RetrieveUpdateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectCreateSerializer  # allows clients & users update
#     permission_classes = [IsAuthenticated]

# 7. Retrieve/Update a single project
class ProjectDetailView(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectCreateSerializer  # for updates
        return ProjectSerializer  # for GET/view



# 8. Assigned projects for the logged-in user
class AssignedProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)
    
#9 Show all projects created by any user
class AllProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()  # Show all projects
    permission_classes = [IsAuthenticated]