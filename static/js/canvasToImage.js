var canvasData = canvas.toDataURL("image/png");
var ajax = new XMLHttpRequest();
ajax.open("POST",'saveImage.php',false);
ajax.setRequestHeader('Content-Type', 'application/upload');
ajax.send(canvasData);
