# BillboardAcademicInternship

Group A Project for Academic Internship.

## Configuration manual

## Step 1: Creating the database

To begin, you will need a Railway account configured with MySQL.

1. Create a Railway account.
2. Select **New Project**.
3. Select **Create Database**.
4. Choose **MySQL**.

Once the database has been created:

1. Open the **Variables** tab.
2. Copy the **Public URL**.

The Public URL will be used to connect to the database through the command line.

Example:

```text
mysql://root:gTbvncHotkVPKvbgXxPCIcmKNxuXaBGy@junction.proxy.rlwy.net:52709/railway
```

The URL contains the following values:

| Value | Description | Example |
|---|---|---|
| Username | Remains as `root` | `root` |
| Password | Between `:` after root and `@` before the hostname | `gTbvncHotkVPKvbgXxPCIcmKNxuXaBGy` |
| Host | Between `@` and the port number | `junction.proxy.rlwy.net` |
| Port | Between `:` after the hostname and `/` | `52709` |
| Database | Remains as `railway` | `railway` |

---

## Step 2: Importing the SQL script

Once you have the database URL, use the values from it to create the import command.

The command format is:

```bash
mysql -h hostname --port portnumber --protocol=TCP -u root -p railway < "db location"
```

Example:

```bash
mysql -h junction.proxy.rlwy.net --port 52709 --protocol=TCP -u root -p railway < "C:\file\location\script.sql"
```

Replace the values with the information from your Railway Public URL and run the command in Command Prompt.

You will then be prompted for the database password.

Enter the password from the Railway Public URL.

Once successful, the Railway database will update with the tables and data from the SQL script.

---

## Step 3: Installing required software

Install the following software:

- Visual Studio Code  
  https://code.visualstudio.com/download

- Docker Desktop  (You don't need an account) (If linux pops up to be installed, follow the instructions)
  https://www.docker.com/products/docker-desktop/

- GitHub Desktop  
  https://desktop.github.com/download/

After installing the software, open Visual Studio Code and press CTRL+SHIFT+X, and search + install these extensions:

- Dev Containers
- Container Tools
- Docker
- Python

Next, clone this GitHub repository by doing the following:
 1. Open GitHub Desktop and click File --> Clone Repository
 2. Click URL and copy this link into the URL form: https://github.com/ChristianJ123ABC/BillboardAcademicInternship
 3. Choose the location where you want to store the Repository
 4. Click Clone once selected

Open the repository folder in Visual Studio Code:

```text
File → Open Folder → GitHub repository folder
```

The folder should be located in a path similar to:

```text
C:\Users\<username>\Documents\GitHub\BillboardAcademicInternship
```

The terminal should show that you are inside this repository folder.

---

## Step 4: Building the container

Before building the container:

1. Copy the `.env` file provided in the submission.
2. Place it inside the cloned repository folder.
3. Open the `.env` file.

Update the values beginning with `MYSQL` using the information from the Railway Public URL.

Example:

```env
MYSQL_HOST=junction.proxy.rlwy.net
```

Use the provided `.env` values from the submission for:

- `TOTP_ENCRYPTION_KEY`
- `STRIPE_SECRET_KEY`
- `SECRET_KEY`
- `MYSQL_CHARSET`

Once all values have been configured:

1. Ensure Docker Desktop is running.
2. Ensure the terminal is inside the repository directory.
3. Run:

```bash
docker compose up --build
```
4. Go to Docker Desktop --> Containers and you should see a start button. Click this and open the "Running on http://127.0.0.1:5000" link.
   
This will build the Docker container and allow the website to run.

---

## Issues
A common issue when running the docker build, will be that it won't be able to find the .env file. If this is the case, make sure the .env file is actually named '.env', instead of just 'env'. If done correctly, the file will actually turn a dark gray in the explorer section like this:


<img width="168" height="302" alt="image" src="https://github.com/user-attachments/assets/8160694c-29ec-44fd-b843-1d6171dc306e" />


If you encounter any issues with the project, contact:

```text
x23524103@student.ncirl.ie
```
## Optional ERD Step: Creating the database using forward engineering

The database can be created from the ERD diagram in the submission using MySQL Workbench's Forward Engineer feature.

Steps:

1. Open the project ERD file in MySQL Workbench.
2. Select:

   Database → Forward Engineer

3. Select the MySQL connection to use.
4. Review the generated SQL script.
5. Execute the generated SQL script.

MySQL Workbench will create the database schema, tables, primary keys, foreign keys, and relationships based on the ERD design.
