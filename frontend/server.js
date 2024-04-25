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

app.get('/facility', (req, res) => {
  res.render('facility', {getData: null}); 
});

app.post('/facility', async(req,res) =>{
  try {
    const response = await axios.get('http://localhost:5000/api/facility');
    console.log(response.data);
    res.render('facility', {getData: JSON.stringify(response.data)});
  }
  catch(error){
    console.log(error);
  }
});

//Teacher APIs
app.get('/teacher', (req, res) => {
  res.render('teacher', {getData: null}); 
});

// GET method
app.post('/teacher/get', async (req, res) => {
  var room_id = parseInt(req.body.room_id_get);
  console.log(room_id);
  
  try {
      // Make API call
      const apiResponse = await axios.get(`http://localhost:5000/api/teacher?room=${room_id}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // RENDER THE PAGE WITH THE DATA
      res.render('teacher', { getData: JSON.stringify(data) });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  } 
});

//POST Method
app.post('/teacher/post', async (req, res) => {
  var room_id = parseInt(req.body.room_id_post);
  var firstname = req.body.firstname_post;
  var lastname = req.body.lastname_post;
  console.log(room_id, firstname, lastname);
  try {
      // Make API call
      const apiResponse = await axios.post(`http://localhost:5000/api/teacher?room=${room_id}&firstname=${firstname}&lastname=${lastname}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // Render EJS template with null data
      res.render('teacher', { getData: null });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
});

//PUT Method
app.post('/teacher/put', async (req, res) => {
  var id = parseInt(req.body.id_put);
  var firstname = req.body.firstname_put;
  var lastname = req.body.lastname_put;
  var room_id = parseInt(req.body.room_id_put)
  console.log(id, firstname, lastname, room_id);
  try {
      // Make API call
      const apiResponse = await axios.put(`http://localhost:5000/api/teacher?id=${id}&firstname=${firstname}&lastname=${lastname}&room=${room_id}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // Render EJS template with null data
      res.render('teacher', { getData: null });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
});

//DELETE Method
app.post('/teacher/delete', async (req, res) => {
  var id = parseInt(req.body.ID_delete);
  console.log(id);
  try {
      // Make API call
      const apiResponse = await axios.delete(`http://localhost:5000/api/teacher?id=${id}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // Render EJS template with null data
      res.render('teacher', { getData: null });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
});


//Child APIs
app.get('/child', (req, res) => {
  res.render('child', {getData: null}); 
});
// GET method
app.post('/child/get', async (req, res) => {
  var room_id = parseInt(req.body.room_id_get);
  console.log(room_id);
  
  try {
      // Make API call
      const apiResponse = await axios.get(`http://localhost:5000/api/child?room=${room_id}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // RENDER THE PAGE WITH THE DATA
      res.render('child', { getData: JSON.stringify(data) });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  } 
});

//POST Method
app.post('/child/post', async (req, res) => {
  var firstname = req.body.firstname_post;
  var lastname = req.body.lastname_post;
  var room_id = parseInt(req.body.room_id_post);
  var age = parseInt(req.body.age_post);
  console.log(firstname, lastname, room_id, age);
  try {
      // Make API call
      const apiResponse = await axios.post(`http://localhost:5000/api/child?firstname=${firstname}&lastname=${lastname}&room=${room_id}&age=${age}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // Render EJS template with null data
      res.render('child', { getData: null });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
});

//PUT Method
app.post('/child/put', async (req, res) => {
  var id = parseInt(req.body.id_put);
  var firstname = req.body.firstname_put;
  var lastname = req.body.lastname_put;
  var age = req.body.age_post
  var room_id = parseInt(req.body.room_id_put)
  console.log(id, firstname, lastname, room_id);
  try {
      // Make API call
      const apiResponse = await axios.put(`http://localhost:5000/api/child?id=${id}&firstname=${firstname}&lastname=${lastname}&age=${age}}&room=${room_id}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // Render EJS template with null data
      res.render('child', { getData: null });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
});

//DELETE Method
app.post('/child/delete', async (req, res) => {
  var id = parseInt(req.body.ID_delete);
  console.log(id);
  try {
      // Make API call
      const apiResponse = await axios.delete(`http://localhost:5000/api/child?id=${id}`);

      // Extract data from API response
      var data = apiResponse.data;
      console.log(data);

      // Render EJS template with null data
      res.render('child', { getData: null });
  } catch (error) {
      // Handle errors
      console.error('Error fetching data:', error);
      res.status(500).send('Error fetching data', error);
  }
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





//start the express application on port 8081 and print server start message
app.listen(port, () => console.log('Application started on localhost:8081'));
