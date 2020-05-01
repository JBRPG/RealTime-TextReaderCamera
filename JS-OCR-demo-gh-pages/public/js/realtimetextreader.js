/*
This will be modified to allow real-time readind of text from the camera

The following aspects are needed to work:

setInterval(func|code, [delay], [args[...]], ...)
Tesseract - automatic image to text recognizer

video
canvas
image (image div section that would be step 2)
fxCanvas
texture



OPTIONAL
clearInterval(timerID; code|func) // can put inside setTimeout (() => clearSettings, delay)

*/
(function() {
    var video = document.querySelector('video');

    var pictureWidth = 640;
    var pictureHeight = 360;

    var fxCanvas = null;
    var texture = null;

    function checkRequirements() {
        var deferred = new $.Deferred();

        //Check if getUserMedia is available
        if (!Modernizr.getusermedia) {
            deferred.reject('Your browser doesn\'t support getUserMedia (according to Modernizr).');
        }

        //Check if WebGL is available
        if (Modernizr.webgl) {
            try {
                //setup glfx.js
                fxCanvas = fx.canvas();
            } catch (e) {
                deferred.reject('Sorry, glfx.js failed to initialize. WebGL issues?');
            }
        } else {
            deferred.reject('Your browser doesn\'t support WebGL (according to Modernizr).');
        }

        deferred.resolve();

        return deferred.promise();
    }

    function searchForRearCamera() {
        var deferred = new $.Deferred();

        //MediaStreamTrack.getSources seams to be supported only by Chrome
        if (MediaStreamTrack && MediaStreamTrack.getSources) {
            MediaStreamTrack.getSources(function(sources) {
                var rearCameraIds = sources.filter(function(source) {
                    return (source.kind === 'video' && source.facing === 'environment');
                }).map(function(source) {
                    return source.id;
                });

                if (rearCameraIds.length) {
                    deferred.resolve(rearCameraIds[0]);
                } else {
                    deferred.resolve(null);
                }
            });
        } else {
            deferred.resolve(null);
        }

        return deferred.promise();
    }

    function setupVideo(rearCameraId) {
        var deferred = new $.Deferred();
        var videoSettings = {
            video: {
                optional: [{
                        width: {
                            min: pictureWidth
                        }
                    },
                    {
                        height: {
                            min: pictureHeight
                        }
                    }
                ]
            }
        };

        //if rear camera is available - use it
        if (rearCameraId) {
            videoSettings.video.optional.push({
                sourceId: rearCameraId
            });
        }

        navigator.mediaDevices.getUserMedia(videoSettings)
            .then(function(stream) {
                //Setup the video stream
                video.srcObject = stream;

                video.addEventListener("loadedmetadata", function(e) {
                    //get video width and height as it might be different than we requested
                    pictureWidth = this.videoWidth;
                    pictureHeight = this.videoHeight;

                    if (!pictureWidth && !pictureHeight) {
                        //firefox fails to deliver info about video size on time (issue #926753), we have to wait
                        var waitingForSize = setInterval(function() {
                            if (video.videoWidth && video.videoHeight) {
                                pictureWidth = video.videoWidth;
                                pictureHeight = video.videoHeight;

                                clearInterval(waitingForSize);
                                deferred.resolve();
                            }
                        }, 100);
                    } else {
                        deferred.resolve();
                    }
                }, false);
            }).catch(function() {
                deferred.reject('There is no access to your camera, have you denied it?');
            });

        return deferred.promise();
    }

    /*********************************
     * Real Time Snapshot Recorder
     *********************************/

    // Functions
    function step1_cameraSetup(){
        checkRequirements()
            .then(searchForRearCamera)
            .then(setupVideo)
            .done(function() {
                //Enable the 'take picture' button
                $('#takePicture').removeAttr('disabled');
                //Hide the 'enable the camera' info
                $('#step1 figure').removeClass('not-ready');
                setInterval(step2_recordSnapShot, 500);
            })
            .fail(function(error) {
                showError(error);
            });
    }

    function step2_recordSnapShot(){
        var canvas = document.querySelector('#step2 canvas');
        var img = document.querySelector('#step2 img');

        //setup canvas
        canvas.width = pictureWidth;
        canvas.height = pictureHeight;

        var ctx = canvas.getContext('2d');

        //draw picture from video on canvas
        ctx.drawImage(video, 0, 0);

        //modify the picture using glfx.js filters
        texture = fxCanvas.texture(canvas);
        fxCanvas.draw(texture)
            .hueSaturation(-1, -1) //grayscale
            .unsharpMask(20, 2)
            .brightnessContrast(0.2, 0.9)
            .update();

        window.texture = texture;
        window.fxCanvas = fxCanvas;
        $(img)
            //show output from glfx.js
            .attr('src', fxCanvas.toDataURL());
        step3_convertToText();

    }

    function step3_convertToText(){
        var canvas = document.querySelector('#step3 canvas');
        var step2Image = document.querySelector('#step2 img');

        var ctx = canvas.getContext('2d');

        // Draw image is required for Tesseract to recognize possible text
        ctx.drawImage(
            step2Image,
            0,
            0,
            canvas.width,
            canvas.height);

        // do the OCR!
        // Also where the DOMException: Security Error is likely triggered
        Tesseract.recognize(ctx).then(function(result) {
            var resultText = result.text ? result.text.trim() : '';
            console.log(resultText);

            //show the result
            $('blockquote p').html('&bdquo;' + resultText + '&ldquo;');
            $('blockquote footer').text('(' + resultText.length + ' characters)');
        });
    }


    //start snapshot recorder immediately
    // then proceed to step 2
    // with a repeating interval every 1 second (1000 ms)
    step1_cameraSetup();



})();
