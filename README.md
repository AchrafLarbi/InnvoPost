# InnovPost - AI-Powered Customer Engagement Solution

## 🏆 About the Project
InnovPost is an innovative platform designed to **enhance customer engagement** for **Algérie Poste**. It empowers customers by providing a **real-time feedback system** while offering administrators **AI-driven insights** into service quality. The system integrates **social media monitoring**, **sentiment analysis**, and an **interactive web dashboard** to help Algérie Poste continuously improve its services.

## 📌 Key Features
- **🌐 Web Dashboard**: Provides real-time insights into customer sentiment and service trends.
- **📊 Social Media Monitoring**: Tracks and analyzes feedback from **Facebook** and **Twitter**.
- **🤖 AI Sentiment Analysis**: Uses NLP models to assess customer satisfaction and detect trending issues.
- **📥 Customer Feedback System**: Collects feedback via QR codes placed at post offices.
- **📡 Data Visualization**: Offers graphical representations of customer trends and service metrics.

## 🔧 Technologies Used
- **Frontend**: React.js / Next.js
- **Backend**: Django / Django REST Framework
- **AI & NLP**: Hugging Face Transformers for Sentiment Analysis
- **Social Media APIs**: Facebook Graph API, Twitter API
- **Database**: PostgreSQL / Firebase

## 🚀 How to Run the Backend Server
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/innovpost.git
   cd innovpost/backend
   ```
2. Set up a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Create a superuser (optional, for admin access):
   ```sh
   python manage.py createsuperuser
   ```
6. Run the backend server:
   ```sh
   python manage.py runserver 0.0.0.0:8000
   ```

## 🤝 Contributing
We welcome contributions! Feel free to submit issues or pull requests. 🎯

## 📜 License
MIT License
