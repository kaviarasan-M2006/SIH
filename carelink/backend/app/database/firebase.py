import os
FIREBASE_ENABLED = False
def init_firebase():
    global FIREBASE_ENABLED
    cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")
    if cred_path and os.path.exists(cred_path):
        FIREBASE_ENABLED = True
    return FIREBASE_ENABLED
