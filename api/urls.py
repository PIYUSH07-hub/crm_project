from django.urls import path
from .views import (
    create_client_form,
    client_list_view,
    UserListView,
    ClientListAPIView,
    ClientListCreateView,
    ClientDetailView,
    ProjectCreateView,
    # UserProjectsView,
    ProjectDetailView,
    AssignedProjectsView, # ✅ ADD THIS for retrieving logged-in user's assigned projects
    AllProjectsView
    )


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # ✅ Clients API
    path('clients/', ClientListCreateView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),

    # ✅ Projects API
    path('projects/create/', ProjectCreateView.as_view(), name='project-create'),
    # path('projects/', UserProjectsView.as_view(), name='user-projects'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    # ✅ Assigned Projects for Logged-in User
    path('my-projects/', AssignedProjectsView.as_view(), name='my-projects'),  
    # ✅ Auth (login)
    path('login/', obtain_auth_token, name='api_token_auth'),

    # ✅ HTML Views (for browser-based forms)
    path('create-client-form/', create_client_form, name='create-client-form'),
    path('client-list-view/', client_list_view, name='client-list-view'),

    # ✅ User List: Lists all users — used when assigning users to projects
    path('users/', UserListView.as_view(), name='user-list'),
    
    #show all Project
    path('all-projects/', AllProjectsView.as_view(), name='all-projects'),
    
]
