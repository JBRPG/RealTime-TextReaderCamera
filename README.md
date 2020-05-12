# 1. Getting App to Run Locally (MacOS)

## Step 1: Install Dependencies
```bash 
# install python requirements
pip install -r requirements.txt

# install OpenCV2
brew install opencv@2

# install Tesseract OCR library
brew install tesseract
```

## Step 2: Clone Repo
```bash
git clone https://github.com/JBRPG/RealTime-TextReaderCamera.git tesseract-letters
```

## Step 3: Run Flask
```bash
cd tesseract-letters
export FLASK_APP=application.py
flask run
# now, navigate to http://127.0.0.1:5000/
```

In order to run the code, you have to ensure that Flask is running. After you get everything installed, you will be able to access your application in the future by just performing Step 3. 


# 2. Getting App to Run on Heroku

## Step 1: Initialization
1. Create a new app on Heroku by logging into the Heroku website and using the Web UI.
1. Using the heroku command line client:
   * Go to your command line and login:<br> `heroku login -i`
   * Connect your local git repo (assumes you have already done this) to your newly created Heroku app:<br> `heroku git:remote -a 'app-you-just-made'`
1. Push your repo to Heroku: `git push heroku master`

This will create your app and install all of the Python dependencies listed in your requirements.txt. It will also read your Procfile and see that you've created a web application (via Flask).

## Step 2: Configuration 
You will need to perform a few more steps in order to get Tesseract and OpenCV to work:

1. Go to the "settings" tab of your application and add the following buildpack:
https://github.com/heroku/heroku-buildpack-apt. This will allow you to install Ubuntu packages (OpenCV, Tesseract, etc.), which can be specified in the Aptfile.
1. For Tesseract, you'll need to create an enviornment variable to point tell the application where the training data is located. Follow [this guide](https://medium.com/@zamhuang/heroku-how-to-install-service-and-setup-environment-variable-use-tesseract-ocr-as-example-d7c708c4ba8d). For my installation, I used the command shown below:<br>`heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata`
1. Performance-wise, I read [this guide](https://devcenter.heroku.com/articles/python-gunicorn#basic-configuration) and update the concurrency environment variable to 3. Tesseract / OpenCV ran WAAAY faster:<br>`heroku config:set WEB_CONCURRENCY=3`

When you're done with these steps, commit your changes and redeploy to Heroku by pushing an empty commit to Heroku:

```bash
git commit --allow-empty -m "empty commit"
git push heroku master
```

# 3. Posting Data to Server (Client-Side)
Please see `static/js/image-capture.js` and `templates/uploader.html` for examples re: how to transmit an image to the server. You can just post directly to the Heroku endpoints from any local file you don't want to create your own server:

## Posting an image from Canvas object
To post an image taken from the canvas object:
### HTML
```html
    <canvas id="my_canvas"></canvas>
```
### JavaScript
```js
const canvas = document.querySelector('#my_canvas');
const binaryImage = canvas.toDataURL("image/png", 0.5);
fetch('https://tesseract-letters.herokuapp.com/', {
    method: "POST",
    body: binaryImage,
    headers: {
        "Content-type": "image/png"
    }
})
.then(response => response.json())
.then(data => {
    console.log(data);
    document.querySelector('#results').innerHTML = JSON.stringify(data);
});
```

## Posting an image from a file upload:
```html
<form method="post" enctype="multipart/form-data" action="https://tesseract-letters.herokuapp.com/uploader/">
    <input type="file" name="file">
    <input type="submit" value="Upload">
</form>
```

