# Airbnb Directory

A full-stack application that provides an interface for browsing and managing Airbnb listings. This project uses Angular (v19.0.4) for the frontend and Flask/MongoDB for the backend.

## 📌 Project Overview

This application allows users to:
- Browse Airbnb listings with pagination
- View detailed information about individual listings
- See property locations on Google Maps with current weather information
- Post and read reviews for properties
- Filter and view properties in a data grid
- Authenticate using Auth0
- Edit and delete listings (for authenticated users)

## 📋 Project Structure

```
airbnbFE/                # Angular frontend application
├── src/                 # Source code
│   ├── app/             # Angular components and services
│   │   ├── airbnb.component.*     # Main listings component
│   │   ├── listing.component.*    # Individual listing component
│   │   ├── grid.component.*       # Grid view component
│   │   ├── nav.component.*        # Navigation component
│   │   ├── auth*.component.*      # Authentication components
│   │   ├── data.service.ts        # Data services
│   │   ├── web.service.ts         # API service
│   │   └── app.*.ts               # App configuration files
│   ├── index.html       # Main HTML file
│   └── main.ts          # Application entry point
└── angular.json         # Angular configuration

blueprints/              # Flask backend blueprints
├── auth/                # Authentication routes
├── hosts/               # Host management
├── listings/            # Listing management
├── reviews/             # Review management
├── users/               # User management
├── geo/                 # Geographic data and services
└── operations/          # Administrative operations

app.py                   # Flask application entry point
decorators.py            # Auth decorators and middleware
globals.py               # Global variables and database connections
```

## 🚀 Getting Started

### Prerequisites

- Node.js (v16+)
- Angular CLI (v19.0.4)
- Python (v3.8+)
- MongoDB
- API Keys:
  - Google Maps API
  - OpenWeatherMap API
  - API Ninjas

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd airbnbFE
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   ng serve
   ```

4. Access the application at `http://localhost:4200/`

### Backend Setup

1. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```
   pip install flask flask-cors pymongo bcrypt pyjwt
   ```

3. Start the Flask server:
   ```
   python app.py
   ```

4. The API will be available at `http://127.0.0.1:5000/`

## 🔑 API Keys

This project uses several external services that require API keys:

1. **Google Maps API** - Used for displaying property locations
   - Located in `src/index.html`
   - Current key: `AIzaSyC69-i8Gcx-1vxaS5Y6xp-HoUeTolNIDfM`

2. **OpenWeatherMap API** - Used for displaying current weather at property locations
   - Located in `src/app/data.service.ts`
   - Current key: `5358fa926cd6340d99ca4b81f9a6ecc9`

3. **API Ninjas** - Used for generating Lorem Ipsum text
   - Located in `src/app/data.service.ts`
   - Current key: `se8iMQVK7YvPwVR2v7pAgQ==XuyjlTXln7YxU6eT`

> ⚠️ **Security Note**: These API keys should not be stored in code in a production environment. Consider using environment variables or a secure key management system.

## 🔐 Authentication

This application uses Auth0 for authentication:
- Domain: `dev-e0wg4rv17ljv4b74.us.auth0.com`
- Client ID: `y25qZ8qHUwdjbSespAtSTkpLi1Z0FDii`

Authentication configuration is in `src/main.ts`.

## 🧪 Testing

### Frontend Testing

Run Angular unit tests with:
```
ng test
```

The project includes test files for components and services with `.spec.ts` extensions.

### Backend Testing

Backend tests are not included in the current codebase but should be added for production use.

## 📚 API Documentation

The backend provides RESTful endpoints with the following structure:

```
/api/v1.0/listings              # Get all listings (paginated)
/api/v1.0/listings/:id          # Get, update, or delete a specific listing
/api/v1.0/listings/:id/reviews  # Get or post reviews for a listing
/api/v1.0/listings/priceRangeSummary  # Get price distribution data
```

Additional endpoints exist for authentication, user management, and operational tasks.

## 🖥️ Features

### Components

- **ListingsComponent**: Displays a paginated grid of property cards
- **ListingComponent**: Shows detailed information about a single listing
- **GridComponent**: Provides a data grid view with filtering
- **NavComponent**: Navigation bar with authentication controls
- **HomeComponent**: Dashboard with price distribution statistics

### Services

- **WebService**: Handles API communication with the backend
- **DataService**: Provides utility functions and external API access
- **AuthService**: Manages authentication with Auth0

## 🛠️ Built With

- [Angular](https://angular.dev/) - Frontend framework
- [Bootstrap](https://getbootstrap.com/) - UI component library
- [AG Grid](https://www.ag-grid.com/) - Data grid component
- [Flask](https://flask.palletsprojects.com/) - Backend framework
- [MongoDB](https://www.mongodb.com/) - Database
- [Google Maps API](https://developers.google.com/maps) - Map integration
- [Auth0](https://auth0.com/) - Authentication provider

## 🚧 Future Improvements

- Add more comprehensive test coverage
- Implement image upload for listings
- Add search functionality
- Improve mobile responsiveness
- Add booking functionality
- Implement user profiles and saved favorites
- Add multilingual support

## 📄 License

This project is licensed under the MIT License
