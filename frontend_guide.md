# VeteranMeet Frontend Development Guide

## Overview
VeteranMeet is a comprehensive Django REST API backend for a veteran community platform. This guide explains the key concepts, data models, API endpoints, and logic to help frontend developers build the user interface effectively.

## Project Architecture
- **Backend**: Django REST Framework with PostgreSQL/SQLite database
- **Authentication**: JWT (JSON Web Tokens) with 24-hour access tokens and 7-day refresh tokens
- **File Uploads**: Support for images (avatars, profile pics, event images, post images)
- **Real-time Features**: Chat functionality (requires WebSocket integration for real-time messaging)

## Core Concepts

### 1. User Management
- **Custom User Model**: Extends Django's AbstractUser with email as username field
- **Profiles**: One-to-one relationship with User, contains bio, images, location, military info
- **Star System**: Users earn stars through events, determining veteran categories
- **Follow System**: Users can follow/unfollow each other

**Veteran Categories** (based on star count):
- Bronze Veteran: < 25,000 stars
- Silver Veteran: 25,000 - 39,999 stars
- Ruby Veteran: 40,000 - 49,999 stars
- Golden Veteran: 50,000 - 59,999 stars
- Diamond Veteran: 60,000 - 64,999 stars
- Sapphire Veteran: 65,000 - 69,999 stars
- Platinum Veteran: 70,000 - 99,999 stars
- Eternal Sage: 100,000+ stars

### 2. Events System
- **Events**: Community gatherings with participants, locations, and star rewards
- **Participation**: Users can join events and earn stars
- **Interest**: Users can mark events as interesting without committing
- **Star Points**: Events award stars to participants (max 5000 per event)

### 3. Social Features
- **Posts**: User-generated content with likes and comments
- **Comments**: Threaded discussions on posts
- **Likes**: Users can like posts

### 4. Communication
- **Chat**: Direct and group chat rooms with message history
- **Notifications**: Real-time alerts for likes, comments, stars, event updates
- **Support Groups**: Private/public groups for peer support with posts

### 5. Resources
- **Resource Categories**: Organized categories for veteran resources
- **Resources**: Links, documents, and information for veterans

### 6. Veteran Hub
- **Announcements**: Priority-based system announcements
- **User Stats**: Dashboard statistics (posts, events joined, connections, resources shared)

## API Endpoints Overview

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token

### Users
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/` - Update current user profile
- `GET /api/auth/users/` - List all users
- `GET /api/auth/users/{user_id}/stars/` - Get user's stars
- `POST /api/auth/give-star/{user_id}/` - Give stars to user
- `POST /api/auth/follow/{user_id}/` - Follow/unfollow user
- `GET /api/auth/feed/` - Get user's personalized feed

### Events
- `GET /api/events/` - List events
- `POST /api/events/` - Create event
- `GET /api/events/{id}/` - Get event details
- `POST /api/events/{id}/join/` - Join event
- `GET /api/events/{id}/participants/` - Get event participants
- `GET /api/events/by-hobbies/` - Filter events by hobbies
- `GET /api/events/by-location/` - Filter events by location
- `POST /api/events/{id}/interested/` - Mark interest in event

### Posts
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/{id}/like/` - Like/unlike post
- `GET /api/posts/{id}/comments/` - Get post comments
- `POST /api/posts/{id}/comments/` - Add comment
- `GET /api/posts/comments/{id}/` - Get comment details

### Notifications
- `GET /api/notifications/` - List user notifications
- `POST /api/notifications/{id}/read/` - Mark notification as read
- `POST /api/notifications/mark-all-read/` - Mark all as read
- `GET /api/notifications/unread-count/` - Get unread count

### Chat
- `GET /api/chat/rooms/` - List chat rooms
- `POST /api/chat/rooms/` - Create chat room
- `GET /api/chat/rooms/{id}/` - Get room details
- `GET /api/chat/messages/` - List messages
- `POST /api/chat/messages/` - Send message

### Support Groups
- `GET /api/support-groups/groups/` - List support groups
- `POST /api/support-groups/groups/` - Create group
- `GET /api/support-groups/groups/{id}/` - Get group details
- `GET /api/support-groups/posts/` - List group posts
- `POST /api/support-groups/posts/` - Create group post

### Resources
- `GET /api/resources/categories/` - List resource categories
- `GET /api/resources/resources/` - List resources
- `POST /api/resources/resources/` - Create resource

### Veteran Hub
- `GET /api/hub/announcements/` - List announcements
- `GET /api/hub/dashboard/` - Get user dashboard
- `GET /api/hub/stats/` - Get user statistics

## Data Structures (Serializers)

### User Data
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "is_veteran": true,
  "profile": {
    "id": 1,
    "bio": "Veteran bio",
    "avatar": "url",
    "profile_pic": "url",
    "location": "City, State",
    "military_branch": "Army",
    "service_years": "2000-2005",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  },
  "stars_count": 15000,
  "veteran_category": "Silver Veteran"
}
```

### Event Data
```json
{
  "id": 1,
  "title": "Veterans Meetup",
  "description": "Monthly gathering",
  "location": "Community Center",
  "city": "New York",
  "event_type": "Social",
  "hobbies_related": "sports,gaming",
  "date_time": "2023-12-01T18:00:00Z",
  "max_participants": 50,
  "star_points": 100,
  "organizer": 1,
  "participants": [1, 2, 3],
  "interested": [4, 5],
  "image": "url",
  "is_active": true,
  "created_at": "2023-11-01T00:00:00Z",
  "updated_at": "2023-11-01T00:00:00Z"
}
```

### Post Data
```json
{
  "id": 1,
  "author": 1,
  "title": "My Story",
  "content": "Post content",
  "image": "url",
  "likes": [1, 2, 3],
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Key Logic and Business Rules

1. **Star System**: Stars are earned through event participation. The total star count determines veteran category.

2. **Event Participation**: Users can join events to earn stars. Each event has a star point value.

3. **Follow System**: Users can follow others to see their posts in their feed.

4. **Notification System**: Triggers for likes, comments, stars received, event joins, and reminders.

5. **Chat Rooms**: Support both direct (1-on-1) and group chats.

6. **Support Groups**: Have privacy levels (public, private, invite-only) and role-based membership (member, moderator, admin).

7. **Resource Management**: Resources are organized into categories for easy browsing.

8. **Dashboard**: Aggregates user activity statistics for personalized experience.

## UI Panels/Pages Structure by User Role

The application has three main user roles with different panel access:

### 1. Regular User Panels (Non-Veteran Users)
**Total: 12 panels**
- **Authentication Panels** (3): Login, Registration, Password Reset
- **Basic Profile Panel** (1): View/edit basic profile (no military info)
- **Limited Social Feed** (2): View public posts, Create basic posts
- **Basic Events** (2): Browse events, View event details (cannot create)
- **Basic Resources** (2): Browse resource categories and resources
- **Basic Communication** (2): Notifications, Basic chat access

### 2. Veteran User Panels (is_veteran=True)
**Total: 25 panels** - Full access to all features
- **All Regular User Panels** (12)
- **Enhanced Profile** (1): Full veteran profile with military info, star ratings
- **Star Management** (1): Give/receive stars, view veteran categories
- **Full Social Features** (2): Follow system, personalized feed
- **Event Management** (2): Create events, manage organized events
- **Support Groups** (3): Create groups, manage memberships, group posts
- **Veteran Hub** (2): Announcements, personal statistics
- **Advanced Communication** (2): Full chat rooms, group creation

### 3. Admin Panels (Django Admin Interface)
**Total: 8 panels** - Administrative access
- **User Management Admin** (2): Manage all users, moderate profiles
- **Content Moderation** (3): Moderate posts, events, support groups
- **System Administration** (2): Announcements management, system stats
- **Resource Management** (1): Manage resource categories and resources

## Detailed Panel Breakdown

### Shared Panels (Available to All Authenticated Users)
- **Dashboard/Home** (1): Personalized dashboard based on user role
- **Profile Management** (1): Varies by user type (basic vs veteran)
- **Notifications** (1): Real-time notifications system
- **Settings** (1): Account settings and preferences

### Veteran-Only Panels (13 additional)
- **Star System Interface** (1): View/give stars, veteran category display
- **Event Creation & Management** (2): Create events, manage participation
- **Support Group Management** (3): Create/manage groups, member roles
- **Advanced Social Features** (2): Follow system, personalized feeds
- **Veteran Hub Features** (2): Priority announcements, detailed stats
- **Full Chat Access** (2): Direct and group chat creation
- **Military-Specific Resources** (1): Veteran-focused resource categories

### Admin-Only Panels (8 panels)
- **User Administration** (2): User approval, profile moderation, ban management
- **Content Moderation** (3): Post moderation, event approval, group oversight
- **System Management** (2): Announcement publishing, analytics dashboard
- **Resource Curation** (1): Add/edit resource categories and resources

**Grand Total: 45 panels/pages** across all user roles

The frontend should implement role-based routing and component visibility based on user permissions and the `is_veteran` field.

## Frontend Implementation Notes

1. **Authentication**: Store JWT tokens securely (localStorage/sessionStorage). Handle token refresh automatically.

2. **File Uploads**: Use multipart/form-data for image uploads. Handle both avatar and profile_pic in user profiles.

3. **Real-time Features**: Implement WebSocket connection for chat and notifications.

4. **Pagination**: Most list endpoints support pagination - implement infinite scroll or page-based loading.

5. **Error Handling**: Handle 401 (unauthorized) by redirecting to login, 403 (forbidden) for permission issues.

6. **State Management**: Consider using Redux/MobX/Vuex for managing user state, notifications, and chat data.

7. **Responsive Design**: Ensure mobile-friendly interface for veteran accessibility.

8. **Accessibility**: Implement proper ARIA labels, keyboard navigation, and screen reader support.

## Development Environment Setup

1. Backend runs on `http://localhost:8000` (default Django port)
2. CORS configured for `http://localhost:3000` (React default)
3. Media files served from `/media/` URL
4. API documentation available at `/api/swagger/`

## Deployment Instructions

### Fly.io Deployment

The application is configured for deployment on Fly.io. Use the following commands to set up environment secrets:

```bash
# Set environment variables using flyctl secrets set KEY=VALUE format
flyctl secrets set SECRET_KEY="your-very-long-random-secret-key-here"
flyctl secrets set DATABASE_URL="postgresql://username:password@hostname:5432/database_name"
flyctl secrets set DEBUG="False"
flyctl secrets set ALLOWED_HOSTS="your-app-name.fly.dev,www.your-app-name.fly.dev"

# Deploy the application
flyctl deploy
```

**Environment Variables Format:**
- **KEY**: `SECRET_KEY` | **VALUE**: `"your-very-long-random-secret-key-here"`
- **KEY**: `DATABASE_URL` | **VALUE**: `"postgresql://username:password@hostname:5432/database_name"`
- **KEY**: `DEBUG` | **VALUE**: `"False"`
- **KEY**: `ALLOWED_HOSTS` | **VALUE**: `"your-app-name.fly.dev,www.your-app-name.fly.dev"`

### Environment Variables Reference

Required environment variables for production:

- `SECRET_KEY`: Django secret key (generate a long random string)
- `DATABASE_URL`: PostgreSQL connection string
- `DEBUG`: Set to "False" for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- `DB_NAME`: Database name (if using separate DB variables)
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port (default: 5432)

### Local Development Setup

For local development, create a `.env` file in the project root:

```env
SECRET_KEY=your-development-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=veteranmeet_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## Testing

Use the provided test files (`test_api.py`, `test_endpoints.py`, etc.) to understand expected API behavior and responses.
