
## Description:
- This is django project which create rest APIs for user authentication and learning_management.
- We have developed **Learning Management System** using **Python Django** and **Postgres**.
- This project contains four modules - Admin, Mentor, Student and Role.
- In this project contains Two Apps:
   1. __Auth__
   2. __management__
    
***1.Auth:***
- This is Authentication App where only Admin will register the user, user can change his password or reset his password.   
- It contains AddRoleAPI,UserRegistrationAPI,UserLoginAPI,UserLogoutAPI,ChangeUserPasswordAPI,ForgotPasswordAPI,ResetPasswordAPI

1. Add Role API -
    - In this add role API Admin can add a role of user.
2. User registration API - 
    - In this API view only admin will register the user.
    - After successfully registered the user, an email is sent to the user's registered email ID with a login credentials.

- In this, we used `Signals` for mapping the user role.
3. User Login API -
    - This API is for logged in the user.
    - For authentication , we used `JWT Token`.
    - Here we store token in `Redis cache`.

**Redis** 
    
- We used Redis for storing token in redis cache.
- If expiry of token is one day, and if user again login in 15 minutes with the same token then he can be successful logged in. So to overcome this problem we used redis.
- When use logout out, token automatically delete from redis cache.

4. User Logout API - 
    - This API is used to log user out and to clear the user session  
    - When user logged out, token will delete from redis cache.
5. Change User Password API -
    - This API is used to change the user password.
6. Forgot Password API -
    - If user forgot his password, then this API is used to send reset password link to user email id.
7. Reset Password API -
    - This API is used to reset the user password after validating jwt token.

***2.management:***
- In this management app contains all the model related to Student, Mentor and Course
- management app provides APIs for following features:
1. AddCourseAPIView - 
    - This API is used to add course by the admin.
2. AllCoursesAPIView - 
    - This API is used to retrieve all courses by an admin.
3. UpdateCourseAPIView - 
   - This API is used to update course by an admin.
4. DeleteCourseAPIView - 
   - This API is used to delete course by id by an admin.
5. CourseToMentorMapAPIView -
   - This API is used to update course to mentor.
6. DeleteCourseFromMentorListAPIView -
   - This API is used to delete course from mentor list.
7. MentorDetailsAPIView -
   - This API is used to get the Specific Mentor Profile if the user is mentor otherwise Admin can see each mentor's Profile
8. StudentCourseMentorMapAPIView -
   - This API is used to post student course mentor mapped record.
9. StudentCourseMentorUpdateAPIView -
   - This API is used to update student course mentor mapping.
10. GetMentorsForSpecificCourse -
    - This API is used to fetch course oriented mentors
11. StudentsAPIView -
    - Using this API Admin can see all course assigned students and mentor can see his course assigned students and student can see his own record
12. StudentDetailsAPIView -
    - This API is used to get Student details as well ass eduction details. Admin can see any student, mentor can see those student under him and student can see his own details
13. StudentsDetailsUpdateAPIView -
    - This API is used to update student basic details.
14. EducationDetails -
    - Using this API admin can see any students educational details, mentor can see his own students details student can see his own details.
15. EducationDetailsAdd -
    - This API is used to add Education details of student. This API is accessible to student only.
16. EducationDetailsUpdate -
    - This API is used to update student educational details.
17. NewStudents -
    - Using this API admin will retrieve new students who have not been assigned to any course yet.
18. StudentPerformance -
    - Using this API student can see his own all performance, mentor can see all students' performance under him and admin can see any students all performance.
19. StudentPerformanceUpdate -
    - This API is used to update student's weekly performance either by mentor or admin.
20. UpdateScoreFromExcel -
    - Update the student score from Excel sheet.
21. AddMentorAPIView -
    -  This API is used for add mentor with course.
22. GetMentorDetailsAPIView -
    - This API used for fetching mentor details.
23. AddStudent -
    - This API is used to Add new user student and mapp mentor, course to it.
24. StudentProfile -
    - This api will show the profile data of students Retrieved by student id
    Accessible by admin,student and for mentors only assigned students under him/her.
25. MentorStudentCourse -
    - This API is used to get the list of students according to mentor_id and course_id.
## To install Requirement packages using:
  
    pip install -r requirements.txt
---
## Start Django Project Creation:

### Project Startup:
- Firstly create project directory folder-
  
  `mkdir Learning_Management_System`
- Create a Virtual Environment-
    
  `python -m venv venv`
- Create django project using:
    
  `django-admin startproject <Project_name>`
- Then create project app using:
        
  `python manage.py startapp <App_name>`

### sample .env

    export APP_SECRET_KEY=
    export DBBACKEND=
    export DBNAME=
    export DBUSER=
    export DBPASSWORD=
    export DBHOST=
    export DBPORT=
    export MAILUSER=
    export MAILPASSWORD=
    export REDISHOST=
    export REDISPORT=
### Database Connection:
- Firstly connect project with postgres database.
  - In setting.py file:
        
        DATABASES = {
             'default': {
                'ENGINE': os.environ.get('DBBACKEND'),
                'NAME': os.environ.get('DBNAME'),
                'USER': os.environ.get('DBUSER'),
                'PASSWORD': os.environ.get('DBPASSWORD'),
                'HOST': os.environ.get('DBHOST'),
                'PORT': os.environ.get('DBPORT'),
            }
        }
    
- Create Models for App :
  - In this project contains Two Apps:
   1. __Auth__
   2. __Management__
- Register App in settings.py file:
  - In setting.py file:
    
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'Auth.apps.AuthConfig',
            'Management.apps.ManagementConfig',
            'drf_yasg',
            'rest_framework',
            'django_celery_results',
        ]
- Register models in admin.py file.
- After creating models, migrate the project:

        python manage.py makemigrations
        python manage.py migrate
---
## Swagger Configuration:
- Firstly installing swagger using:

      pip install -U drf-yasg
- Additionally, if you want to use the built-in validation mechanisms, you need to install some extra requirements:

      pip install -U drf-yasg[validation]
- We need to configured swagger -
  - Add swagger in setting.py-Install_Apps -
  
        INSTALLED_APPS = [
                  ...
                  'django.contrib.staticfiles',
                  'drf_yasg',
                  ...
              ]
 - Then in root urls.py file add following code:

        from rest_framework import permissions
        from drf_yasg.views import get_schema_view
        from drf_yasg import openapi
        
        schema_view = get_schema_view(
            openapi.Info(
                title="Fundoo_Note",
                default_version='v1',
                description="Test description",
                terms_of_service="https://www.google.com/policies/terms/",
                contact=openapi.Contact(email="contact@fundoonote.local"),
                license=openapi.License(name="Test License"),
            ),
            public=True,
            permission_classes=(permissions.AllowAny,),
        )
        urlpatterns = [
            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        ]
---
- Create Serializer class.
- Create API Views.
---
## Celery:
- **Celery**:
  - Celery is a task queue based on distributed message passing.
  - Celery communicate via message broker to mediate between clients and workers. By default, celery used rabbitmq as a message broker.
- we need to install celery using:
  `pip install celery`
- In the project root folder create one new file- celery.py file and add the following code:
  
      import os
      from celery import Celery

      os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

      app = Celery('project_name')
      app.config_from_object('django.conf:settings', namespace='CELERY')
      app.autodiscover_tasks()
- NOw edit the init.py file in the project root:
  
      from .celery import app as celery_app
      __all__ = ['celery_app']
- Then in django app create tasks.py file and write the celery tasks.
    - Basic tasks
      

      from celery import shared_task

      @shared_task
      def name_of_your_function(optional_param):
          pass  # do something heavy
- Starting The Worker Process : Open a new terminal tab, and run the following command:
  
   `celery -A myproject worker -l info`
---
## RabbitMQ:
- **RabbitMQ**:
  - RabbitMQ is a message broker. It accepts and forward messages. 
- We need to install RabbitMQ:
  - To download and install the RabbitMQ, click Here: 
  [link](https://www.rabbitmq.com/install-windows.html)
- We also need to install Erlang for RabbitMQ:
  - To install Erlang, click here: 
  [link](https://erlang.org/download/otp_versions_tree.html)
- After successfully installation:
  - Click on the start button and open rabbitmq cmd prompt.
  - After opening, enables the plugins using:
    `rabbitmq-plugins enable rabbitmq_management`
  - Now run the rabbitmq : http://localhost:15672
  - Use the following credentials for authentication: 
    - username : guest
    - password : guest
---  
### Deploy application on AWS
- Click on the following link to know how to deploy django application on AWS
[link](https://docs.google.com/document/d/1j1fh9MCJDG2gybPfs9Zk0Kvp5i9Q6u3ys6PrL9UU1G4/edit?usp=sharing)

###Author
1. Bharti Mali
2. Archana Bhamare
3. Ranjith P
4. Ronali Panigraphy
5. Birajit Nath



     