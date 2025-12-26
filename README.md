# StoryLens MVP

**Turn your favorite memories into timeless narratives.**

StoryLens is a privacy-first, AI-powered application that transforms user-uploaded photos into personalized narrative stories. It uses **OpenAI's GPT-4o Vision** API to analyze images and generate empathetic, context-aware stories based on user-provided metadata.

## Key Features

* **Privacy First**: No long-term storage of user images. Photos are processed and strictly deleted immediately after story generation.
* **Vision AI**: Leveraging GPT-4o Vision for deep understanding of visual context, emotions, and atmosphere.
* **Lean MVP**: A single, streamlined web flow—upload, contextualize, and read.
* **Fast Response**: Optimized for low latency using the latest Chat Completions API.

## Project Structure

```bash
story-lens/
├── app/
│   ├── main.py              # Application entry point (Flask)
│   ├── services/
│   │   └── vision_service.py # Core Vision AI logic
│   ├── utils/
│   │   └── file_handler.py   # Secure file handling & cleanup
│   └── templates/
│       └── index.html        # Frontend MVP interface
├── redundants/               # Archived legacy code
├── requirements.txt          # Python dependencies
├── run.py                    # Dev server runner
└── README.md                 # Documentation
```

## Setup & Installation

1. **Clone the repository**:

    ```bash
    git clone <your-repo-url>
    cd story-lens
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment**:
    Create a `.env` file in the root directory:

    ```bash
    cp .env.example .env
    ```

    Populate it with your keys:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    FLASK_ENV=production
    ```

5. **Run Development Server**:

    ```bash
    python run.py
    ```

    Access the app at `http://127.0.0.1:5000`.

## Deployment

For production, use a WSGI server like **Gunicorn**:

1. Install Gunicorn:

    ```bash
    pip install gunicorn
    ```

2. Run the application:

    ```bash
    gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
    ```

    * `-w 4`: Uses 4 worker processes for concurrency and faster response handling.
    * `-b 0.0.0.0:8000`: Binds to port 8000 on all interfaces.

### Optimization Tips

* **GPT-4o**: We use the standard `gpt-4o` model which offers a great balance of speed and intelligence. For even faster responses (with slightly less nuance), you can switch the model in `app/services/vision_service.py` to `gpt-4o-mini` if available.
* **Concurrency**: Gunicorn workers allow handling multiple requests simultaneously, essential for a web service.

## Tech Stack

* **Backend**: Python, Flask
* **AI**: OpenAI GPT-4o (Vision + Chat Completions)
* **Frontend**: HTML5, CSS3 (Privacy-First UI)
* **Infrastructure**: Stateless, Ephemeral Storage

---
*Note: Legacy services from previous iterations (Tripetto integration, MidJourney generation) have been archived in the `redundants/` directory.*
