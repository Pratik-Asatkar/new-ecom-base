import cloudinary
import cloudinary.uploader

import config.secrets as secrets

# Cloudinary configuration

cloudinary.config(
    cloud_name=secrets.CLOUD_NAME,
    api_key=secrets.API_KEY,
    api_secret=secrets.API_SECRET,
    secure=True
)


def upload(file, file_name, foldername):
    try:
        result = cloudinary.uploader.upload(
            file=file, public_id=file_name,
            folder=foldername, unique_filename=False
        )

        return result
    except Exception as e:
        print(f"Error/upload: {e}")
        return False
