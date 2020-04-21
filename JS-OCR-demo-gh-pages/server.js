//jshint esversion:6
//jshint multistr:true

const hbs = require( 'express-handlebars');
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.urlencoded({extended: true}));
const port = 3000;

app.set('view engine', 'hbs');


app.engine('hbs', hbs({
    extname: 'hbs',
    layoutsDir: __dirname + '/views/layouts',
}));

//Serves static files (we need it to import a css file)
app.use(express.static('public'))

/*
Cannot get the local server to run the open source demo
on filename nor local servers
*/

// app.get('/', function (req, res){
//     res.sendFile(__dirname + "/../index.html");
// });

app.get('/', (req, res) => {
    //Serves the body of the page aka "main.handlebars" to the container //aka "index.handlebars"
    res.render('main', {layout : 'index'});
});

app.listen(port, function() {
    //console.log(__dirname);
    console.log(`Example app listening at http://localhost:${port}`);
});
