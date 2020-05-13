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
1. Go to your command line and login: `heroku login -i`
1. Using the heroku command line client, connect your local repo to your newly created Heroku app: `heroku git:remote -a 'app-you-just-made'`
1. Push your repo to Heroku: `git push heroku master`

This will create your app and install all of the Python dependencies listed in your requirements.txt. It will also read your Procfile and see that you've created a web application (via Flask).

## Step 2: Configuration
You will need to perform a few more steps in order to get Tesseract and OpenCV to work:

1. Go to the "settings" tab of your application and add the following buildpack:
https://github.com/heroku/heroku-buildpack-apt. This will allow you to install Ubuntu packages (OpenCV, Tesseract, etc.), which can be specified in the Aptfile.
1. For Tesseract, you'll need to create an enviornment variable to point tell the application where the training data is located. Follow [this guide](https://medium.com/@zamhuang/heroku-how-to-install-service-and-setup-environment-variable-use-tesseract-ocr-as-example-d7c708c4ba8d). For my installation, I used the command shown below:

```bash
heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata
```

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

# Extra Features

## /uploader/ Endpoint

In the application.py file, you should see the endpoint with the word "uploader", which serves as testing ground for Tesseract to recognize text. All you have to do is choose an image file (png, jpg, jpeg, gif, bmp), and then click on "upload" to generate results. The images should consist of letter tiles that are close enough to the camera to be recognized as letters. Once an image is chosen, Tesseract will read the image to find as many matching words possible. After reading the image, the results will be shown as an array of letters scanned in clusters.

## recognize_text.py file Case Settings

There is currently no frontend solution to allow the user to configure letter recognition. However, if you want to experiment with letter, there are three settings:

* Lower Case
* Upper Case
* Both Lower and Upper Cases

These options are represented by the following lines:

```python
# tessdata_dir_config = '--psm 10 --oem 1 -c tessedit_char_whitelist=' + lower_case
# tessdata_dir_config = '--psm 10 --oem 1 -c tessedit_char_whitelist=' + upper_case
# tessdata_dir_config = '--psm 10 --oem 1 -c tessedit_char_whitelist=' + upper_case + lower_case

# '#' is a comment, and you pick one line to uncomment
# to allow Tesseract to read data based on case settings
```

# Questions, Feedback, Comments

Feel free to provide feedback, questions, and comments about this project. We look forward to hearing from you.
