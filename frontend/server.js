//load express module
const express = require('express');
const path = require('path');

//put new express application on app variable
const app = express();
app.use(express.json());
app.use(express.urlencoded({extended:false}));

//axios
const axios = require('axios');
const config = {
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  }
};

//set views property and views engine
app.set("views", path.resolve(__dirname, "views"));
app.set("view engine", "ejs");

const port = 8081;

var auth = false;

app.get('/teacher', (req, res) => {
  res.render('teacher'); // Assuming you have a teacher.ejs file in your views folder
});

app.get('/child', (req, res) => {
  res.render('child'); // Assuming you have a teacher.ejs file in your views folder
});

//force user to login if not authorized
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

app.post('/login', async(req,res)=>{

  // get login info from ejs form
  const { username, password } = req.body;

  // attempt login
  try {
    const response = await axios.post("http://localhost:5000/api/login", {username, password});
    
    console.log(response.data)

    //redirect to home page if login attempt is successful
    if(response.data.message == 'Login successful'){
      auth = true;
      res.redirect('/');
    }
    else {
      res.redirect('/login?error=invalid_credentials')
    }

  }
  // catch error if login failed
  catch(error){
    console.log("Error during login:", error);
    res.redirect('/login?error=login_failed');
    
  }
});

app.post('/teacher/get', async (req, res) => {
  try {
      // Make API call
      const apiResponse = await axios.get('http://localhost:5000/api/teacher/all');

      // Extract data from API response
      const data = apiResponse.data;
      console.log(data);
      // Render EJS template with data
      res.render('teacher', { data });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
});

//start the express application on port 8081 and print server start message
app.listen(port, () => console.log('Application started on localhost:8081'));