const mongoose = require('mongoose');
const express = require('express');
var cors = require('cors');
const bodyParser = require('body-parser');
const logger = require('morgan');
const Data = require('./data');

const API_PORT = 3002;
const app = express();
app.use(cors());
const router = express.Router();

// this is our MongoDB database
const dbRoute = 'mongodb+srv://test:test@cluster-hinbg.gcp.mongodb.net/test?retryWrites=true&w=majority';


var MongoClient = require('mongodb').MongoClient;
var url = dbRoute;

router.get('/getData', (req, res) => {
  MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("uber");
  dbo.collection("uber").find({}).toArray(function(err, result) {
    if (err) throw err;
    console.log(result);
    return res.json({ success: true, data: result });  
  db.close();
  });
});
});


// append /api for our http requests
app.use('/api', router);

// launch our backend into a port
app.listen(API_PORT, () => console.log(`LISTENING ON PORT ${API_PORT}`));
