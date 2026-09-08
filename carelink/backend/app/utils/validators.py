ALLOWED_FILE_TYPES = ["pdf", "jpg", "jpeg", "png", "mp4", "wav"]
MAX_FILE_SIZE_MB = 25
def is_allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED_FILE_TYPES
def is_valid_size(size_bytes: int) -> bool:
    return size_bytes <= MAX_FILE_SIZE_MB * 1024 * 1024
