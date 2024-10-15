# 📚 NYT Bestsellers & Amazon Book Finder 📘

Welcome! This project allows users to discover books recommended by the **New York Times** and provides a direct link to purchase them on **Amazon**. 🛒

The system integrates **FastAPI** on the backend and **React** on the frontend, all containerized with **Docker** for easy setup and deployment. Below are the instructions on how to run the project, along with some important implementation details.

---

## 🌟 Main Features:

1. **Search by genre:** Filter books based on their genre.
2. **NYT API integration:** Fetch the latest bestsellers directly from the New York Times API.
3. **Amazon purchase link:** Click on any book to view or buy it directly on Amazon.
4. **Background process:** The app requests and stores bestselling books from each genre in the background.
5. **Retry policies:** The system retries failed API requests up to 5 times if a `429 Too Many Requests` error is encountered.
6. **In-memory storage:** All data is stored in memory for simplicity and performance.
7. **Execution logs:** Detailed logs of all API interactions and background processes.

---

## 🚀 How to Run the Project

Follow these steps to run the project on your local machine:

### 1. 📦 Clone the repository:

```bash
git clone https://github.com/username/nyt-amazon-book-finder.git
cd nyt-amazon-book-finder
```

### 2. 📄 Create a `.env` file for the NYT API key:

Navigate to the `backend/` directory (where the **Dockerfile** is located) and create a `.env` file with the following content:

```bash
NYT_API_KEY=your_nyt_api_key_here
```

Make sure to replace `your_nyt_api_key_here` with your actual **New York Times** API key.

### 3. 🐳 Build and run the containers with Docker:

This project comes fully containerized, so you can run it with a single command:

```bash
docker-compose up --build
```

This will build and launch both the backend (FastAPI) and the frontend (React).

### 4. 🌐 Access the application:

Once Docker finishes building, open your browser and visit:

```bash
http://localhost:3000
```

You will now be able to search for books and explore NYT’s bestsellers.

---

## 🧠 Important Details

- **Background task:** When the application starts, it requests all available genres from the **NYT API** and stores the bestsellers for each genre in memory. This process runs in the background and makes API calls sequentially for each genre. 

- **Data loading time:** Initially, only a few genres may be available in the frontend, as it takes time to retrieve and store the bestsellers for each genre. As the app continues running, more genres and their books will appear in the interface.

- **Retry policies:** If a `429 Too Many Requests` error occurs while calling the NYT API, the system will retry up to **5 times** almost immediately. If the API still does not return a successful response (`200`), the application will stop trying, and no further attempts to load the data will be made during that session.

---

## 📚 Backend (FastAPI) Details

The backend is powered by **FastAPI** and handles the following tasks:

- **Background process:** Fetches all genres and bestsellers from the NYT API, storing them in memory.
- **Logging:** Logs all API interactions and background processes for easier debugging.
- **Retry policies:** Handles rate-limited responses by retrying failed requests up to 5 times.
- **API endpoint:** Provides a clean endpoint for the frontend to consume book data.

---

## 🎨 Frontend (React + TypeScript) Details

The user interface is built with **React** and **TypeScript**. Key features include:

- **Search by genre:** Users can filter books by different genres.
- **Book details:** The UI presents book titles, authors, and a direct link to Amazon for purchasing.
- **Responsive design:** The interface is responsive, minimalist, and user-friendly.

---

## 🛠️ Technologies Used:

- **Backend:** FastAPI, Python
- **Frontend:** React, TypeScript
- **Docker:** Manages the entire deployment process.
- **Error Handling & Logging:** Ensures smooth user experience and easy debugging in production.

---

## 📐 Sequence Diagrams

- **NYT API Integration:** Describes the process of querying and updating the bestseller data.
- **Amazon Integration:** Illustrates a potential future integration with Amazon's API for product details.
- **O'Reilly Integration:** Outlines a possible approach for fetching technical book prices from O'Reilly.

---

## 🧪 Testing

The project includes basic tests to ensure the core functionalities work correctly:

1. **Unit tests** for critical functions.
2. **Integration tests** to verify that the frontend and backend communicate properly.

To run the tests, use the following command inside the FastAPI container:

```bash
docker exec -it backend pytest
```

---

## 🎉 Conclusion

Thank you for exploring the **NYT Bestsellers & Amazon Book Finder**. We hope this tool provides a seamless way to discover and purchase new books.

If you have any questions, suggestions, or encounter any issues, feel free to open an issue or reach out. 😊
