# mvfi_web

### Prerequisites:

- Python 3.7
- virtualenv
- ffmpeg (`brew install ffmpeg`)

### Environment setup:
 
```
brew install ffmpeg
git clone git@github.com:calmoo/flask_mvfi.git
cd flask_mvfi
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
 
### Build setup:

```
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```
