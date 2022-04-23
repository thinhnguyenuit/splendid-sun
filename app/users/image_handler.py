import os
from typing import Any

from flask import current_app
from PIL import Image


def add_profile_image(image: Any, username: str) -> str:
    ext_type = image.filename.split[-1]
    profile_img = f"{username}.{ext_type}"
    filepath = os.path.join(
        current_app.root_path, "static", "profile_imgs", profile_img
    )

    output_size = (200, 200)

    img = Image.open(image)
    img.thumbnail(output_size)
    img.save(filepath)

    return profile_img
