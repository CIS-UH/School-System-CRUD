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
  const userLoginInfo = req.body;

  console.log(userLoginInfo);

  // attempt login
  try {
    const response = await axios.post("http://localhost:5000/api/login", userLoginInfo);
    
    console.log(response.data)

    //redirect to home page if login attempt is successful
    if(response.data.message == 'Login successful'){
      auth = true;
      res.redirect('/');
    }


  }
  // catch error if login failed
  catch(error){
    console.log("login failed");
    
  }
});


//start the express application on port 8081 and print server start message
app.listen(port, () => console.log('Application started on localhost:8081'));