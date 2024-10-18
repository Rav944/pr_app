
# Running the Project and Testing the Functionality

## Step 1.1: Start the Application Using Docker Compose

To get started, we will run the application using Docker Compose. Make sure you have Docker and Docker Compose installed on your system.

1. Clone the repository:

    ```bash
    git clone git@github.com:Rav944/pr_app.git
    cd pr_app
    ```

2. Run the application using Docker Compose:

    ```bash
    docker-compose up --build
    ```

3. Once the services are running, access the web container's bash environment:

    ```bash
    docker exec -it <your_web_container_name> bash
    ```

## Step 1.2: Create a Django Superuser

To log into the Django admin panel, you will need a superuser. Inside the web container, create one:

```bash
python manage.py createsuperuser
```

Follow the prompts to provide a username, email, and password.

## Step 1.3: Fetch Available Images from the API

While still inside the web container, run the command to fetch images from the external API:

```bash
python manage.py fetch_images
```

This command will pull all available images from the API and save their metadata into the database as `Image` objects.

## Step 1.4: Access the Admin Panel and Add Test Data

1. Open your browser and navigate to the Django admin panel at: `http://localhost:8000/admin/`.
2. Log in using the superuser credentials you created earlier.

## Step 1.5: Create Test Users and Chats

1. In the admin panel, go to the **Users** section and create several test users.
2. Then, navigate to the **Chats** section and create a chat for each of the users you just created. Each user should have one unique chat.

## Step 1.6: Test the Image Messaging Functionality

1. In the admin panel, go to the **Images** section where the fetched images are listed.
2. Select the images you would like to send as messages.
3. From the action dropdown at the top, select **Send selected images as messages to all chats** and click **Go**.
4. This action will send the selected images to all user chats as messages.

You can check the messages sent to each chat in the **Messages** section of the admin panel.

---

# Ideas for Future Updates

## 2.1: Image Storage in the Database

Currently, images are only stored as URLs fetched from the external API. To improve reliability, especially if we plan to stop relying on the API, it would be beneficial to save the images locally in our database or file storage. This can be implemented by:
- Adding a backup mechanism that downloads and saves images when they are fetched from the API.
- Storing these images either in a local file system or a cloud storage solution like AWS S3, and updating the image model to point to the local backup if necessary.

## 2.2: Application Scaling and Modularization

As the project grows, we should refactor the codebase for better scalability and maintainability. Some ideas include:
- **Modularizing the views**: Instead of having all views in a single `views.py` file, split it into multiple modules by feature. For example, create a `views` folder and have files like `chat_views.py`, `message_views.py`, etc.
  
    Example structure:
    ```
    pru_app/
    └── chat/
        └── views/
            ├── chat_views.py
            ├── message_views.py
            └── image_views.py
    ```

- **Adding Nginx**: Introduce Nginx as a reverse proxy to manage web traffic and improve performance. Nginx will handle requests and proxy them to the Django application, which is particularly useful in production environments.

- **Background Task Management with Celery**: For any long-running tasks such as sending messages to a large number of users, integrating Celery for background job processing would improve user experience and scalability. Celery, combined with Redis or RabbitMQ as a message broker, can handle tasks asynchronously.

    Tasks that could be managed by Celery:
    - Sending mass messages.
    - Fetching and backing up images.
    - Any future batch processing or notifications.

## 2.3: Logging and Monitoring

As the application grows, it would be useful to add robust logging and monitoring:
- **Logging**: Implement structured logging to keep track of events like API requests, image fetching, and message sending. These logs can be stored locally during development and in a centralized logging service like Logstash or AWS CloudWatch in production.
- **Monitoring**: Sentry, Datadog.
