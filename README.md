# Vehicle Management System

## To run this program, you need to follow a set of requirements first:

### 1. Python
   - Make sure Python is installed on your system. You can download it from [here](https://www.python.org/downloads/).
   - Check Python version by running:
     ```bash
     python --version
     ```

### 2. XAMPP
   - Download and install XAMPP to set up Apache and MySQL for the database. You can get it from [here](https://www.apachefriends.org/index.html).

### 3. Import the Database to PhpMyAdmin
   - Open PhpMyAdmin and import the provided SQL database file.

### 4. Any IDE or Text Editor (I use VS Code)
   - VS Code can be downloaded from [here](https://code.visualstudio.com/).

### 5. Node.js and npm
   - Ensure Node.js and npm are installed. You can download them from [here](https://nodejs.org/).

### 6. Create a Python Virtual Environment and Install Dependencies

   To ensure the project runs correctly, you need to create a Python virtual environment and install the necessary dependencies.

   #### Steps:
   1. **Navigate to the project folder**:
      ```bash
      cd vms
      ```

   2. **Create a virtual environment**:
      - On Windows:
        ```bash
        python -m venv myenv
        ```

   3. **Activate the virtual environment**:
      - Type in console:
        ```bash
        myenv\Scripts\activate
        ```

   4. **Install the dependencies from `requirements.txt`**:
      ```bash
      pip install -r requirements.txt
      ```

### 7. Set Up Environment Variables

   1. **Copy the `.env.example` file to `.env`**:
      ```bash
      cp .env.example .env
      ```
      - This will create a new `.env` file with default settings. You need to update the `.env` file with your actual database credentials and other environment variables.

### 8. Install npm Dependencies and Build CSS

   1. **Install npm dependencies**:
      ```bash
      npm install
      ```

   2. **Build CSS with Tailwind**:
      ```bash
      npm run build:css
      ```
      - Note that you may have to run this every time you make an update with the design.
### 9. Set Up a Self-Signed SSL Certificate for Flask

follow these steps to generate and configure a self-signed certificate.

   #### Steps for Linux:
   1. **Create the necessary directories**:
      ```bash
      sudo mkdir -p /etc/ssl/certs /etc/ssl/private
      ```

   2. **Generate the private key and certificate**:
      ```bash
      sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
          -keyout /etc/ssl/private/selfsigned-key.pem \
          -out /etc/ssl/certs/selfsigned-cert.pem
      ```

   3. **Set proper permissions**:
      ```bash
      sudo chmod 600 /etc/ssl/private/selfsigned-key.pem
      sudo chmod 644 /etc/ssl/certs/selfsigned-cert.pem
      ```

   4. **IF IT SAYS PERMISSION DENIED**:
      - Try running it as root or configure your user to run as an admin.
   #### Steps for Windows:
   1. **Copy the certs folder from the cloned repository**
      - It should be able to run now.


### 10. Run the Flask App

   1. **Run the Flask app**:
      - Run the application with:
        ```bash
        python app.py
        ```
        - Ensure that XAMPP Control Panel is also running with Apache and MySQL turned on.

That's it! The app should now be running locally on your system.
