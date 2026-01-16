# Django Blog Project

A full-featured blog application built with Django 5 and Docker. This project provides a robust platform for publishing articles with rich text editing, category organization, and view tracking.

## Features

*   **Article Management**: Create, edit, and publish articles with a powerful rich text editor (CKEditor 5).
*   **Categories**: Organize content into hierarchical categories/topics.
*   **Rich Media**: Support for image uploads and article thumbnails.
*   **View Tracking**: Tracks article views based on user IP to provide basic analytics.
*   **Search & Filtering**: Search articles by title, content, or category.
*   **Admin Dashboard**: Fully functional Django admin interface for managing content.
*   **Dockerized**: Complete development environment using Docker and Docker Compose.
*   **PostgreSQL**: formatting Production-ready database integration.

## Technology Stack

*   **Backend**: Python 3.11, Django 5.2
*   **Database**: PostgreSQL 16
*   **Frontend**: Django Templates (HTML/CSS)
*   **Infrastructure**: Docker, Docker Compose
*   **Key Libraries**:
    *   `django-ckeditor-5`: For rich text editing.
    *   `pillow`: For image processing.
    *   `gunicorn`: WSGI server.

## Installation & Setup

### Prerequisites

*   Docker
*   Docker Compose

### Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Build and start the services:**
    This command will build the Docker images and start the Django web server alongside the PostgreSQL database.
    ```bash
    docker-compose -f docker-compose.dev.yml up --build
    ```

3.  **Access the application:**
    Once the containers are running, open your browser and visit:
    *   **Main Site**: [http://localhost:8000](http://localhost:8000)
    *   **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)

### Managing Data

**Create a Superuser**:
To access the admin panel, you'll need a superuser account. Run this command in a new terminal window while the containers are running:
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```
Follow the prompts to set a username and password.

**Run Migrations**:
Database migrations are usually handled automatically, but if you need to run them manually:
```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
```

## Project Structure

*   `blog/`: The main Django project configuration.
*   `blog/core/`: The core application containing models and views for the blog functionality.
    *   `models.py`: Defines `Article`, `Category`, `ArticleView` models.
    *   `views.py`: Handles business logic for listing and viewing articles.
*   `docker/`: Docker configuration files.

## License

[MIT License](LICENSE)
