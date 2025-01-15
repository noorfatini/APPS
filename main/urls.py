# Import necessary modules for URL routing
from django.urls import path
# Import Django's built-in LoginView for handling user login
from django.contrib.auth.views import LoginView
# Import views from the current application
from . import views

# Define URL patterns for the application
urlpatterns = [
    # Utility URLs
    # Root URL, maps to the index view and names the URL pattern 'home'
    path('', views.index, name="home"),
    # URL for the about page, maps to the about view and names the URL pattern 'about'
    path('about/', views.about, name='about'),
    
    # User Authentication URLs
    # URL for user registration, maps to the register view and names the URL pattern 'register'
    path('register/', views.register, name="register"),
    # URL for user login, uses Django's LoginView with a custom template and names the URL pattern 'login'
    # path('login', LoginView.as_view(template_name="main/login.html"), name="login"),
    
    path('login', views.login, name="login"),

    # URL for user logout, maps to the logout_view and names the URL pattern 'logout'
    path('logout', views.logout_view, name='logout'),
    # URL for editing user profiles, includes a dynamic 'id' parameter and names the URL pattern 'edit-profile'
    path('edit-profile/<id>', views.edit_profile, name='edit-profile'),
    
    # User Management URLs
    # URL for reading user data, maps to the read_user view and names the URL pattern 'read-user'
    path('read-user', views.read_user, name='read-user'),
    # URL for creating a new user, maps to the create_user view and names the URL pattern 'create-user'
    path('create-user', views.create_user, name='create-user'),
    # URL for updating user information, includes a dynamic 'id' parameter and names the URL pattern 'update-user'
    path('update-user/<id>', views.update_user, name='update-user'),
    # URL for deleting a user, includes a dynamic 'id' parameter and names the URL pattern 'delete-user'
    path('delete-user/<id>', views.delete_user, name='delete-user'),
    
    # Production Plan Management URLs
    # URL for getting a list of production plans, maps to the get_plan_list view and names the URL pattern 'get-plan-list'
    path('get-plan-list', views.get_plan_list, name='get-plan-list'),
    # URL for inputting variables for a production plan, includes a dynamic 'plan_ID' parameter and names the URL pattern 'input_plan_variables'
    path('input_plan_variables/<plan_ID>', views.input_plan_variables, name='input_plan_variables'),
    # URL for deleting a production plan, includes a dynamic 'plan_ID' parameter and names the URL pattern 'delete_plan'
    path('delete_plan/<plan_ID>', views.delete_plan, name='delete_plan'),
    # URL for initiating optimization of a production plan, includes a dynamic 'plan_ID' parameter and names the URL pattern 'initiate_plan_optimize'
    path('initiate_plan_optimize/<plan_ID>', views.initiate_plan_optimize, name='initiate_plan_optimize'),
    # URL for initiating sensitivity analysis of a production plan, includes a dynamic 'plan_ID' parameter and names the URL pattern 'initiate_sensitivity_analysis'
    path('initiate_sensitivity_analysis/<plan_ID>', views.initiate_sensitivity_analysis, name='initiate_sensitivity_analysis'),
    # URL for generating a report for a production plan, includes a dynamic 'plan_ID' parameter and names the URL pattern 'generate_report'
    path('generate_report/<plan_ID>', views.generate_report, name='generate_report'),
]