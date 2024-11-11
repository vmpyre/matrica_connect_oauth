# OAuth FastAPI Integration for Matrica Connect
This project demonstrates a FastAPI app with OAuth 2.1 PKCE authentication flow, utilizing Matrica's OAuth for user authentication. **Don't use this in production.**

## Features
- **OAuth 2.1 PKCE Authentication**: Secure authentication using Proof Key for Code Exchange (PKCE).
- **FastAPI Integration**: Built with FastAPI, a high-performance Python web framework.
- **Jinja2 Templating**: Customizable HTML templates for the authorization and error pages.
- **Async HTTP Requests**: Uses `httpx` for asynchronous HTTP requests to the Matrica API.

## Prerequisites
- Python 3.7+
- Matrica oauth credentials

## Getting Started
### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies
It is recommended to create a virtual environment before installing dependencies:
```bash
python -m venv myenv
source venv/bin/activate  # On Windows use `myenv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file to store your environment variables, following the `.env.sample` file as a reference. Add your `CLIENT_ID` and `CLIENT_SECRET`:
```bash
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
```

### 4. Configure Matrica Redirect URL
In your Matrica dashboard, make sure the Redirect URL is set to:
```bash
http://localhost:8000/callback
```

### 5. Run the Application
Start the FastAPI server:
```bash
python main.py
```
The application will run on `http://localhost:8000` by default. Navigate to the URL and try out the matrica connect follow. This code will fetch the authorized user's connected wallets on success.