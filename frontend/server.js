//load express module
const express = require('express');
const path = require('path');

//put new express application on app variable
const app = express();

//axios
const axios = require('axios');

//set views property and views engine
app.set("views", path.resolve(__dirname, "views"));
app.set("view engine", "ejs");

flaskApi = 'https://localhost:5000/your-endpoint';

const port = 8081;

var auth = false;

//when user hits home page, then we show the hello.ejs page
app.get('/', (req, res) => {
  if(!auth){
    res.redirect('/login');
  }
  
  else{
    res.render('welcome');
  }
});

app.get('/login', (req, res) => {

    res.render('login');

});

app.post('/login', (req,res)=>{
  const userData = req.body;

  try {
    const response = axios.post("https:localhost:5000/api/login", userData)
    console.log('login successful')
    auth = true
    res.redirect('/')
  }
  catch(error){
    console.error("login failed:", error);
    
  }
})


//start the express application on port 8081 and print server start message
app.listen(port, () => console.log('Application started on localhost:8081'));