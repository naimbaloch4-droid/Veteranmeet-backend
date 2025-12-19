# VeteranMeet Django API

A Django REST API for a veteran community platform with user profiles, events, posts, and notifications.

## Features

- **User Management**: Custom user model with veteran profiles and star rating system
- **Events**: Create and join events with participant management
- **Posts**: Social media-style posts with likes and comments
- **Notifications**: Real-time notification system for user interactions
- **JWT Authentication**: Secure token-based authentication

## Setup

1. **Install PostgreSQL** and create a database named `veteranmeet_db`

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database** in `veteranmeet/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'veteranmeet_db',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET/PUT /api/auth/profile/` - User profile management
- `GET /api/auth/users/` - List all users
- `POST /api/auth/star/<user_id>/` - Give/remove star to user

### Events
- `GET/POST /api/events/` - List/create events
- `GET/PUT/DELETE /api/events/<id>/` - Event detail operations
- `POST /api/events/<id>/join/` - Join/leave event
- `GET /api/events/<id>/participants/` - List event participants

### Posts
- `GET/POST /api/posts/` - List/create posts
- `GET/PUT/DELETE /api/posts/<id>/` - Post detail operations
- `POST /api/posts/<id>/like/` - Like/unlike post
- `GET/POST /api/posts/<id>/comments/` - List/create comments
- `GET/PUT/DELETE /api/posts/comments/<id>/` - Comment detail operations

### Notifications
- `GET /api/notifications/` - List user notifications
- `POST /api/notifications/<id>/read/` - Mark notification as read
- `POST /api/notifications/mark-all-read/` - Mark all notifications as read
- `GET /api/notifications/unread-count/` - Get unread notifications count

## Models

### User & Profile
- Custom user model with email authentication
- Profile with bio, avatar, location, military info
- Star rating system between users

### Event
- Event creation with date, location, participant limits
- Many-to-many relationship with users through EventParticipant

### Post
- Posts with content and optional images
- Like system and nested comments
- Chronological ordering

### Notification
- Automatic notifications for likes, comments, stars, event joins
- Read/unread status tracking

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Development

- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL with psycopg2
- JWT authentication with djangorestframework-simplejwt
- CORS enabled for frontend integration