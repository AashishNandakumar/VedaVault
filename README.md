# VedaVault

> Crowdsourced Digital Library of Indian Vedas and Scriptures

1. VedaVault aims to create a comprehensive digital library of ancient Indian Vedas, scriptures, and books through
   crowdsourcing.
2. It will allow people to upload scanned images or digital copies of rare manuscripts, books, or documents related to
   Vedas and other Indian religious/philosophical texts.
3. Users can browse and access the digital library to view, study, or purchase the uploaded content. A portion of the
   proceeds will go to the content contributors.
4. The project will focus on digitizing and preserving important works and commentaries by scholars.
5. VedaVault will make these ancient texts accessible globally, enabling enthusiasts, researchers, and students to
   explore India's rich scriptural heritage.
6. Advanced features like searchable metadata, annotations, and cross-linking with related texts can enhance the user
   experience.
7. Rigorous validation and quality checks will be done to ensure authenticity of the uploaded content.
8. The digital library can be expanded to include translations, transliterations, and scholarly works on Vedas and
   Indian philosophy.

> Built using Django, React.Js and AWS

## Getting Started
> The following instructions currently work only in Linux systems.

These instructions will get your copy of the project up and running on your local machine for development and testing
purposes.

### Clone the Project

1. Clone the project in your machine by:

   ```bash
   git clone https://github.com/AashishNandakumar/VedaVault.git
   ```

### Initial Configurations and Settings

We have used Docker for containerizing our application for efficient replication across different systems for easier
setup.

1. Navigate to the `VedaVault` directory by (Important for all other Instructions):
    ```bash
    cd VedaVault
    ```
2. Setup Docker in your machine by executing the bash script:
    ```bash
   bash docker_commands.bash
   ```
3. Verify Docker and Docker-Compose is installed in your machine by:
   ```bash
   docker --version
    ```
   and
    ```bash
   docker-compose --version
    ```

### Setting up Environment Configurations

1. Create a .env file by:
    ```bash
   touch .env
    ```

2. Open the .env file:
    ```bash
   nano .env
    ```
3. Fill it with the following Environment variables:
    ```bash
    MYSQL_USER='your_username'
    MYSQL_PASSWORD='your_password'
    MYSQL_ROOT_PASSWORD='your_root_password'
    MYSQL_DATABASE_NAME='your_database_name'
    ```

### Building the Image

1. Build the Application's Images by running:
    ```bash
    docker-compose up --build
    ```
2. Stop the Container(keyboard shortcut):
    ```bash
    ctrl + c
    ```
3. Launch a Container from the Image built
   ```bash
   docker-compose up
   ```
   
4. You should now see something like this in the terminal:

   ```bash
   Starting development server at http://0.0.0.0:8000/
   ```

5. Click on the link or copy-paste the link into the browser.

### Interacting with the application

1. Goto the following url to see the list of available endpoints:
   ```bash
   http://0.0.0.0:8000/docs
   ```

2. Use the endpoints as necessary.
