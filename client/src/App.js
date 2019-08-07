// /client/App.js
import React, { Component } from 'react';
import { Map, Marker, Popup, TileLayer } from 'react-leaflet'

class App extends Component {
  // initialize our state
  state = {
    data: [],
    lat: 0,
    lon: 0,
    message: null,
    intervalIsSet: false,
    idToDelete: null,
    idToUpdate: null,
    objectToUpdate: null,
  };

  // when component mounts, first thing it does is fetch all existing data in our db
  // then we incorporate a polling logic so that we can easily see if our db has
  // changed and implement those changes into our UI
  componentDidMount() {
    this.getDataFromDb();
    if (!this.state.intervalIsSet) {
      let interval = setInterval(this.getDataFromDb, 1000);
      this.setState({ intervalIsSet: interval });
    }
  }

  // never let a process live forever
  // always kill a process everytime we are done using it
  componentWillUnmount() {
    if (this.state.intervalIsSet) {
      clearInterval(this.state.intervalIsSet);
      this.setState({ intervalIsSet: null });
    }
  }

  // just a note, here, in the front end, we use the id key of our data object
  // in order to identify which we want to Update or delete.
  // for our back end, we use the object id assigned by MongoDB to modify
  // data base entries

  // our first get method that uses our backend api to
  // fetch data from our data base
  getDataFromDb = () => {
    fetch('http://localhost:3002/api/getData')
      .then((data) => data.json())
      .then((res) => this.setState({ data: res.data }));
  };


  // here is our UI
  // it is easy to understand their functions when you
  // see them render into our screen
  render() {
    const { data } = this.state;
     console.log(data)
    const position = [40.75, -74.09]
return (
      <div id="mapContainer">
      <Map center={position} zoom={11}>
        <TileLayer attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' 
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
        <Marker position = { data.length<=0?position : [ data[0].clusterCenters[0][0],data[0].clusterCenters[0][1]  ] }>
        <Popup>{ data.length<=0? null : `Alrededor de esta zona se han solicitado ${data[0].clusterWeights[0]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[1][0],data[0].clusterCenters[1][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[1]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[2][0],data[0].clusterCenters[2][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[2]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[3][0],data[0].clusterCenters[3][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[3]} ubers` }</Popup>        
</Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[4][0],data[0].clusterCenters[4][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[4]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[5][0],data[0].clusterCenters[5][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[5]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[6][0],data[0].clusterCenters[6][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[6]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[7][0],data[0].clusterCenters[7][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[7]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[8][0],data[0].clusterCenters[8][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[8]} ubers` }</Popup>
        </Marker>
<Marker position = { data.length<=0?position : [ data[0].clusterCenters[9][0],data[0].clusterCenters[9][1]  ] }>
 <Popup>{ data.length<=0? null :`Alrededor de esta zona se han solicitado ${data[0].clusterWeights[9]} ubers` }</Popup>

        </Marker>
      </Map>
      </div>
    )

  }
}
export default App;
