# FastAPI Dynamic Endpoint Generator

This project is a FastAPI application that dynamically generates endpoints from registered functions. It includes an example function that uses OpenAI's GPT API to translate text into Chinese.

## Features

- Dynamically register and expose functions as endpoints.
- Modular design for adding new functions easily.
- Real-world integration with OpenAI GPT for language translation.

## Installation

### Using Python Locally

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your OpenAI API key:
   Replace `YOUR_OPENAI_API_KEY` in `app/functions/translation_function.py` with your actual API key.

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Open Swagger UI to test the API:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t fastapi-dynamic-endpoints .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 fastapi-dynamic-endpoints
   ```

3. Access the API:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Adding New Functions

1. Create a new file in the `app/functions` folder, e.g., `new_function.py`.
2. Define your Pydantic models and function logic in the file.
3. Register the function using `AIFunctions.register()`.
4. The endpoint will be automatically created when the app restarts.

## Example API Request and Response

### Endpoint: `/translate`

#### Request
```json
{
  "text": "Hello, how are you?"
}
```

#### Response
```json
{
  "translated_text": "你好，你好吗？"
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
