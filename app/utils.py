import os
import secrets
from app import app
from PIL import Image



def save_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex + f_ext
	picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
	form_picture.save(picture_path)

	return picture_fn

def save_post_picture(form_picture):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_picture.filename)
	picture_fn=random_hex + f_ext
	picture_path=os.path.join(app.root_path,'static/post_pics',picture_fn)
	form_picture.save(picture_path)

	return picture_fn