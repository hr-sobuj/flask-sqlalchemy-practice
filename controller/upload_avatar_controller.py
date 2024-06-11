from app import app 
from middleware.login_required import login_required
from flask import request,jsonify
from db.db import db
import datetime
from .custom_error import custom_error
import os

@app.patch("/avatar")
@login_required
def upload_avatar():
    try:
        user=g.user
        data=request.files['file']
        file_name=data.filename
        file_split=file_name.split('.')
        file_extention=file_split[len(file_split)-1]
        current_time=datetime.datetime.now()
        file_unique_name = f"{current_time.strftime('%Y%m%d_%H%M%S_%f')}.{file_extention}"


        upload_dir=os.path.join(app.config["UPLOAD_DIR"])
        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        file_path=os.path.join(upload_dir,file_unique_name)
        data.save(file_path)
        user.avatar=file_path
        db.session.commit()
        return jsonify({
            'message': 'Avatar uploaded successfully!'
        })
    except FileNotFoundError as e:
        return custom_error({"error": "Directory not found", "message": str(e)}, 404)
    except Exception as e:
        return custom_error({"error": "Internal Server Error", "message": str(e)}, 500)
