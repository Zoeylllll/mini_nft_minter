from flask import Flask, render_template, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置保存NFT数据的文件
DATA_FILE = 'nfts.json'

# 设置图片上传的目录
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_nfts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_nfts(nfts):
    with open(DATA_FILE, 'w') as f:
        json.dump(nfts, f)

@app.route('/')
def index():
    nfts = load_nfts()
    return render_template('index.html', nfts=nfts)

@app.route('/mint', methods=['GET', 'POST'])
def mint():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        image_file = request.files.get('image_file')
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(image_path)
            image_url = '/' + image_path
        else:
            image_url = ''

        nfts = load_nfts()
        nfts.append({
            'name': name,
            'description': description,
            'image_url': image_url
        })
        save_nfts(nfts)

        return redirect(url_for('index'))

    return render_template('mint.html')

if __name__ == '__main__':
    app.run(debug=True)
