# 📊 YouTube Analytics Dashboard (Grafana Edition)

This project is a YouTube Analytics Dashboard I built to help analyze and visualize how the **LuxDev YouTube channel** is performing over time. It pulls data directly from the YouTube Data API and presents key metrics in an interactive, easy-to-understand way using **Grafana**.

The idea behind this project was to help the creators know key metrics at a glance.

---

## 🔍 What This Dashboard Can Do

- Track how your channel has grown over time  
- Highlight videos that are the most engaging with their audience  
- Show best days and time to post videos  

---

## 🛠️ Tools and Tech Used

Here's a quick overview of the tools that power the dashboard:

- **Python** – Core language for backend and data handling  
- **Apache Airflow** – For orchestrating data extraction and loading workflows  
- **YouTube Data API v3** – Source of all the channel and video data  
- **PostgreSQL** – Stores the processed data  
- **Grafana** – Used to build the dashboard interface  

---

## 🧱 Project Architecture

This project is designed as a lightweight analytics pipeline for YouTube data:

1. **Data Extraction**  
   - A Python script (`controller.py`) pulls data from the YouTube Data API.  
   - This script can be triggered manually or scheduled via Airflow (`dags/` directory).

2. **Data Storage**  
   - Extracted data is sent to a **PostgreSQL** database.  
   - Each metric (views, likes, comments, etc.) is stored with timestamps for trend tracking.

3. **Data Visualization**  
   - **Grafana** is connected to PostgreSQL as a data source.  
   - The dashboards display real-time and historical insights, including:
     - Subscriber growth
     - Top-performing videos
     - Upload frequency
     - Engagement patterns over time

---

## 🗂️ Project Structure

```
youtube_analytics_dashboard/
│
├── dags/               # Airflow DAGs for scheduling data extraction
├── controller.py       # Handles API interactions and data processing
├── main.py             # Entry point for running the application
├── requirements.txt    # List of dependencies
└── README.md           # This file
```

---

## ⚙️ Getting Started

To run this project locally, follow the steps below:

### 1. Clone the repository

```bash
git clone https://github.com/Aminkay95/youtube_analytics_dashboard.git
cd youtube_analytics_dashboard
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure YouTube API credentials

- Go to the [Google Developer Console](https://console.developers.google.com/)
- Enable the **YouTube Data API v3**
- Create an API key or OAuth client ID
- Add your credentials to a `.env` file or export them as environment variables

> If you need help with this part, I've included a `.env.example` file in the repo as a guide.

### 5. Set up PostgreSQL

Ensure you have a PostgreSQL database set up and update the connection details in your environment variables.

### 6. Run Airflow

Initialize the Airflow database and start the scheduler and webserver:

```bash
airflow db init
airflow scheduler
airflow webserver --port 8080
```

Access the Airflow UI at [http://localhost:8080](http://localhost:8080) to monitor and manage your DAGs.

### 7. Set up Grafana

- Install Grafana and configure it to connect to your PostgreSQL database.
- Import the provided dashboard JSON file to visualize your YouTube analytics.

---

## 📝 What's Next / Improvements to Come

Some of the features I’m planning to work on or polish further:

- Weekly summary via email  

---

## 🤝 Want to Contribute?

If you have ideas to improve the dashboard or want to add something new, feel free to fork the project and open a pull request. I’m always open to feedback or collaboration.

---

## 📄 License

This project is open source under the [MIT License](LICENSE), so feel free to use or build on it as long as you give credit.

---

## 📬 Contact

If you have any questions or want to connect, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/amin-kay/) or just open an issue here on GitHub.
