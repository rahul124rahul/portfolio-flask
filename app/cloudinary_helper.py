"""
Cloudinary file upload helper.
Handles uploading images and files to Cloudinary cloud storage.
"""
import cloudinary
import cloudinary.uploader
from flask import current_app


def init_cloudinary():
    """Initialize Cloudinary with app credentials."""
    cloudinary.config(
        cloud_name=current_app.config.get("CLOUDINARY_CLOUD_NAME"),
        api_key=current_app.config.get("CLOUDINARY_API_KEY"),
        api_secret=current_app.config.get("CLOUDINARY_API_SECRET"),
    )


def upload_image(file, folder="portfolio"):
    """
    Upload image to Cloudinary.

    Args:
        file: File object from request.files
        folder: Cloudinary folder name (default: "portfolio")

    Returns:
        URL of uploaded image, or None if upload fails
    """
    try:
        init_cloudinary()

        if not file or not file.filename:
            return None

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=f"portfolio/{folder}",
            resource_type="auto",
            overwrite=True,
        )

        return result.get("secure_url")
    except Exception as e:
        current_app.logger.error(f"Failed to upload image to Cloudinary: {e}")
        return None


def upload_resume(file):
    """
    Upload resume PDF to Cloudinary.

    Args:
        file: File object from request.files

    Returns:
        URL of uploaded resume, or None if upload fails
    """
    try:
        init_cloudinary()

        if not file or not file.filename:
            return None

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder="portfolio/resumes",
            resource_type="auto",
            overwrite=True,
        )

        return result.get("secure_url")
    except Exception as e:
        current_app.logger.error(f"Failed to upload resume to Cloudinary: {e}")
        return None
