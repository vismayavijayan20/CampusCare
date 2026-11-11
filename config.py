import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable is not configured."
        )

    # Database configuration
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        os.path.join(BASE_DIR, "instance", "college.db")
    )

    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + DATABASE_PATH.replace("\\", "/")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Image upload configuration
    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "static", "uploads")
    )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024