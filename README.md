# Event Management API

A comprehensive **Event Management System API** built with Django and Django REST Framework (DRF). This project provides JWT-secured REST endpoints for creating and managing events, RSVP management, and event reviews with advanced permission controls and pagination.

## 📋 Features

- **User Profiles**: Extended Django User model with bio, location, and profile pictures  
- **Event Management**: Full CRUD operations with public/private event support  
- **RSVP System**: Track user attendance status (Going, Maybe, Not Going)  
- **Reviews & Ratings**: Users can review and rate events  
- **JWT Authentication**: Secure all endpoints with token-based authentication  
- **Custom Permissions**: Organizer-only edit/delete and private event access control  
- **Pagination**: Efficient listing of events and reviews  
- **Search & Filtering**: Find events by title, location, or organizer (optional feature)  

## 🛠 Tech Stack

| Technology | Version |
|---|---|
| Python | 3.10+ |
| Django | 5.x |
| Django REST Framework | 3.14+ |
| JWT (SimpleJWT) | Latest |
| SQLite (dev) | - |

## ⚙️ Prerequisites

Before running the project, ensure you have:
- Python 3.10 or higher installed
- pip (Python package manager)
- Git
- Virtual environment tool (venv)

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Sourabh-Narvariya/event-management-api.git
cd event-management-api
```

### Step 2: Create and Activate Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
# Follow the prompts to create an admin account
```

### Step 6: Start Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🔐 Authentication

### Getting JWT Tokens

1. **Obtain Access Token**:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
   ```

2. **Response**:
   ```json
   {
       "access": "eyJhbGciOiJIUzI1NiIs...",
       "refresh": "eyJhbGciOiJIUzI1NiIs..."
   }
   ```

3. **Use Token in Requests**:
   ```bash
   curl -H "Authorization: Bearer <access_token>" \
     http://127.0.0.1:8000/api/events/
   ```

4. **Refresh Token** (when access token expires):
   ```bash
   curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "<refresh_token>"}'
   ```

## 📍 API Endpoints

### Event Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/events/` | Create a new event | ✅ Yes |
| GET | `/api/events/` | List all public events (paginated) | ❌ No |
| GET | `/api/events/{id}/` | Get event details | ❌ No |
| PUT | `/api/events/{id}/` | Update event (organizer only) | ✅ Yes |
| PATCH | `/api/events/{id}/` | Partial update (organizer only) | ✅ Yes |
| DELETE | `/api/events/{id}/` | Delete event (organizer only) | ✅ Yes |

### RSVP Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/events/{event_id}/rsvp/` | RSVP to an event | ✅ Yes |
| PATCH | `/api/events/{event_id}/rsvp/{user_id}/` | Update RSVP status | ✅ Yes |
| GET | `/api/rsvps/` | List user RSVPs | ✅ Yes |

### Review Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/events/{event_id}/reviews/` | Add review for event | ✅ Yes |
| GET | `/api/events/{event_id}/reviews/` | List reviews for event (paginated) | ❌ No |
| GET | `/api/reviews/{id}/` | Get single review | ❌ No |
| PUT | `/api/reviews/{id}/` | Update review (author only) | ✅ Yes |
| DELETE | `/api/reviews/{id}/` | Delete review (author only) | ✅ Yes |

## 🔒 Permissions & Security

### Event Access Control
- **Public Events**: Visible to all authenticated and unauthenticated users  
- **Private Events**: Only the organizer and invited users can view/access  
- **Edit/Delete**: Only the event organizer can modify or delete their events  

### RSVP Permissions
- Users can only update their own RSVP status  
- Organizer can view all RSVPs for their event  

### Review Permissions
- Users can create reviews only for existing events  
- Users can only update/delete their own reviews  
- Reviews are visible to all users  

## 📦 Project Structure

```
event-management-api/
├── eventapi/
│   ├── settings.py          # Django settings with DRF & JWT config
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── events/
│   ├── models.py            # Event, RSVP, Review, UserProfile models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # ViewSets and custom views
│   ├── permissions.py       # Custom permission classes
│   ├── urls.py              # App-specific URL routing
│   ├── admin.py             # Django admin configuration
│   └── tests.py             # Unit tests (optional)
├── manage.py
├── requirements.txt         # Python dependencies
└── README.md
```

## 📝 Usage Examples

### Create an Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Meetup",
    "description": "Join us for a Python discussion",
    "location": "New York",
    "start_time": "2025-12-15T18:00:00Z",
    "end_time": "2025-12-15T20:00:00Z",
    "is_public": true
  }'
```

### RSVP to an Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/1/rsvp/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "Going"}'
```

### Add a Review
```bash
curl -X POST http://127.0.0.1:8000/api/events/1/reviews/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comment": "Great event!"
  }'
```

### List Events with Pagination
```bash
curl "http://127.0.0.1:8000/api/events/?page=1&page_size=10"
```

## 🧪 Testing (Bonus)

If tests are implemented, run them using:
```bash
python manage.py test
# or with pytest
pytest
```

## 📧 Celery & Async Tasks (Bonus)

For email notifications on event updates:
1. Ensure Celery is configured in `settings.py`
2. Start Celery worker:
   ```bash
   celery -A eventapi worker -l info
   ```

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/your-feature`)
2. Commit changes (`git commit -m 'Add feature'`)
3. Push to branch (`git push origin feature/your-feature`)
4. Open a Pull Request

## 📄 License

This project is open-source and available under the MIT License.

## 👨‍💻 Author

**Sourabh Narvariya**  
- GitHub: [@Sourabh-Narvariya](https://github.com/Sourabh-Narvariya)  

## 📞 Support

For issues, questions, or suggestions, please create an issue in the [GitHub repository](https://github.com/Sourabh-Narvariya/event-management-api/issues).

---

**Happy coding! 🚀**
