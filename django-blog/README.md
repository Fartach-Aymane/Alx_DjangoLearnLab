# Django Blog Project

This is a simple blog application built with Django. It allows users to create, read, update, and delete blog posts and comments.

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd django-blog
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```
   python manage.py migrate
   ```

5. **Run the development server:**
   ```
   python manage.py runserver
   ```

6. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage Guidelines

- To create a new blog post, navigate to the post creation page.
- You can view all posts on the post list page.
- Click on a post title to view its details and comments.
- Admin users can manage posts through the Django admin interface.

## Project Structure

```
django-blog/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── blog_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── posts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── tests.py
│   └── migrations/
│       └── __init__.py
├── templates/
│   ├── base.html
│   └── posts/
│       ├── post_list.html
│       ├── post_detail.html
│       └── post_form.html
└── static/
    └── posts/
        └── css/
            └── styles.css
```

## License

This project is licensed under the MIT License.