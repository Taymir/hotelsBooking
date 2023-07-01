from app.tasks.celery import celery
from PIL import Image
from pathlib import Path


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized = im.resize((1000, 500))
    im_resized_thumb = im.resize((200, 100))
    im_resized.save(f"app/static/images/im_resized_{im_path.name}")
    im_resized_thumb.save(f"app/static/images/im_thumb_{im_path.name}")