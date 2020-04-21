//jshint esversion:6
//jshint multistr:true

const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.urlencoded({extended: true}));
const port = 3000;

/*
Cannot get the local server to run the open source demo
on filename nor local servers
*/

app.get('/', function (req, res){
    res.sendFile(__dirname + "/../index.html");

});

app.listen(port, function() {
    //console.log(__dirname);
    console.log(`Example app listening at http://localhost:${port}`);
});
