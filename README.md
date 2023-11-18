# Room Temperature Flask API

Welcome to the Room Temperature Flask API! This API allows you to manage and retrieve temperature data for different rooms. Follow the quickstart guide below to set up and run the API on your local machine.

## Quickstart

1. **Setup Environment Variables:**
    - Create a `.env` file at the root of your project.
    - Add a `DATABASE_URL` variable in the `.env` file, pointing to your PostgreSQL database.

2. **Create Virtual Environment:**
    ```bash
    python3.11.2 -m venv .venv
    ```

3. **Activate Virtual Environment:**
    ```bash
     source ".venv/Scripts/activate"  # (Use a different command on Mac)
    ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the App:**
    ```bash
    flask run
    ```

6. **Access the API:**
    Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to check if the server is running.

## API Endpoints

### 1. Create a Room

- **Endpoint:** `POST /api/room`
- **Request Payload:**
    ```json
    {
        "name": "Room_Name"
    }
    ```
- **Response:**
    ```json
    {
        "id": room_id,
        "message": "Room Room_Name created."
    }
    ```
    - HTTP Status: 201 Created

### 2. Add Temperature Reading

- **Endpoint:** `POST /api/temperature`
- **Request Payload:**
    ```json
    {
        "room_id": room_id,
        "temperature": temperature,
        "date": "mm-dd-yyyy HH:MM:SS"  // Optional, defaults to current time
    }
    ```
- **Response:**
    ```json
    {
        "message": "Temperature added."
    }
    ```
    - HTTP Status: 201 Created

### 3. Global Average Temperature

- **Endpoint:** `GET /api/average`
- **Response:**
    ```json
    {
        "average": global_average,
        "days": number_of_days
    }
    ```
    - HTTP Status: 200 OK

### 4. Room Details

- **Endpoint:** `GET /api/room/{room_id}`
- **Response:**
    ```json
    {
        "name": "Room_Name",
        "average": room_average,
        "days": number_of_days
    }
    ```
    - HTTP Status: 200 OK

### 5. Room Temperature Trends

- **Endpoint:** `GET /api/room/{room_id}?term={term}`
    - `term` can be "week" or "month"
- **Response:**
    ```json
    {
        "name": "Room_Name",
        "temperatures": [
            {"reading_date": "mm-dd-yyyy", "average": temperature},
            // Additional readings...
        ],
        "average": room_average
    }
    ```
    - HTTP Status: 200 OK

Feel free to explore and integrate these endpoints into your application to manage and monitor room temperatures effectively. If you have any questions or issues, don't hesitate to reach out. Happy coding!
