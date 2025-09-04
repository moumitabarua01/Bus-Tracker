pip # Bus Tracking System

A real-time bus tracking system built with Django and Arduino, featuring both web interface and hardware components for accurate bus location tracking and management.

## 🚌 Features

- **Real-time Bus Tracking**
  - Live GPS location tracking
  - Interactive map interface
  - Real-time location updates

- **User Management**
  - User registration and authentication
  - Different user roles (Admin, Driver, Passenger)
  - Personalized dashboards

- **Bus Management**
  - Bus schedule management
  - Route information
  - Driver assignments

- **Hardware Integration**
  - GPS module for location tracking
  - GSM module for data transmission
  - Arduino-based tracking device

## 🛠️ Technology Stack

### Backend
- Django 4.2.11
- Django REST Framework 3.14.0
- Python-dotenv for environment variables
- Geopy for geographical calculations
- Folium for map rendering

### Hardware
- Arduino
- GPS Module
- GSM Module

## 📋 Prerequisites

- Python 3.x
- Arduino IDE
- Git
- Virtual Environment

## 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mehedinaeem/bus_tracker.git
   cd bus_tracker
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # OR
   source venv/bin/activate     # On Unix/macOS
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the root directory and add:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Hardware Setup

1. **Components Required**
   - Arduino Board
   - GPS Module
   - GSM Module
   - Power Supply
   - Connecting Wires

2. **Arduino Configuration**
   - Open `Bus_tracker_hardware/bus_tracker.ino` in Arduino IDE
   - Update `config.h` with your settings
   - Upload the code to your Arduino board

## 📱 Usage

1. **Admin Dashboard**
   - Access at `/admin`
   - Manage buses, routes, and users
   - View tracking data

2. **User Interface**
   - Register/Login at `/bus/registration`
   - View bus locations at `/tracker/map`
   - Check schedules at `/bus/registration/schedule`

## 🗂️ Project Structure

```
bus_tracker/
├── bus/                    # Bus management app
├── tracker/                # Location tracking app
├── bus_tracker/           # Main project settings
├── Bus_tracker_hardware/  # Arduino code and hardware configs
├── static/                # Static files
├── templates/             # HTML templates
└── manage.py             # Django management script
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Mehedi Naeem** - *Initial work* - [mehedinaeem](https://github.com/mehedinaeem)

## 🙏 Acknowledgments

- Thanks to all contributors who have helped with the project
- Special thanks to the Django and Arduino communities for their excellent documentation