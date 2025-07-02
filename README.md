установите зависимости:
            
    pip install -r requirements.txt


создайте .env файл



Пример:

        UPLOAD_DIR="uploads"
        MAX_FILE_SIZE=104857600
        ALLOW_EXT='[".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt", ".mp4", ".mp3", ".zip"]'
        BASE_URL="http://127.0.0.1:8000"
        DB_USERNAME="postgres"
        DB_PASSWORD="pass1234"
        DB_HOST="localhost"
        DB_NAME="url_for_files"



запустите сервер:

        uvicorn main:app --reload --port 8000
