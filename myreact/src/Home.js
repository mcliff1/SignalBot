import React, { Component } from 'react';
import { ObjectInspector, TableInspector } from 'react-inspector';
import ReactJson from 'react-json-view';
import { JsonEditor } from 'react-json-edit';
import { render } from 'react-dom';
import { Chart } from 'react-google-charts';
import BotChart from './BotChart.js';


var mydata = [
  { deivceid : 'bot2', CreatedAt: '2018-04-30 12:23:34', temp: 76.2, humidity: 26.1 },
  { deivceid : 'bot2', CreatedAt: '2018-05-02 12:23:34', temp: 76.4, humidity: 26.0 },
  { deivceid : 'bot2', CreatedAt: '2018-05-05 12:23:34', temp: 76.6, humidity: 26.0 },
];



var mydata = [
{"beg": "beg", "soilmoisture1": 3274.1247255622106, "bottype": "soil", "soilmoisture2": 3175.1096242331837, "soilmoisture3": 2578.5454259691796, "tempc": 30.796327555154228, "battery": 33.427733389278316, "deviceid": "1600aaaaffff0061", "tempf": 80.5677449690722, "volts": 6.954768988153674, "humidity": 19.892216299843522, "CreatedAt": "2018-05-03 12:23:34"}, {"beg": "beg", "soilmoisture1": 3267.938623417472, "bottype": "soil", "soilmoisture2": 3173.7498416365506, "soilmoisture3": 2578.8472637141294, "tempc": 30.79168747795165, "battery": 32.72386002291308, "deviceid": "1600aaaaffff0061", "tempf": 80.5070478174702, "volts": 6.97322181626109, "humidity": 19.882237496321714, "CreatedAt": "2018-05-03 12:23:48"}, {"beg": "beg", "soilmoisture1": 3269.604807068043, "bottype": "soil", "soilmoisture2": 3180.7115081231445, "soilmoisture3": 2579.8048316696627, "tempc": 30.91349889600696, "battery": 32.91031186709302, "deviceid": "1600aaaaffff0061", "tempf": 80.35202682014672, "volts": 6.970779553140899, "humidity": 19.895292757506102, "CreatedAt": "2018-05-03 12:24:00"}, {"beg": "beg", "soilmoisture1": 3268.1887284868158, "bottype": "soil", "soilmoisture2": 3179.766829020895, "soilmoisture3": 2588.692646573567, "tempc": 30.819158521188392, "battery": 33.60084482516983, "deviceid": "1600aaaaffff0061", "tempf": 80.27986394451564, "volts": 6.971174577661359, "humidity": 19.889563807490713, "CreatedAt": "2018-05-03 12:24:13"}, {"beg": "beg", "soilmoisture1": 3256.874787909703, "bottype": "soil", "soilmoisture2": 3183.3744875370044, "soilmoisture3": 2586.986083832782, "tempc": 30.805541967720135, "battery": 33.83118630220724, "deviceid": "1600aaaaffff0061", "tempf": 80.43475613213707, "volts": 6.965575978924227, "humidity": 19.887207789776546, "CreatedAt": "2018-05-03 12:24:27"}, {"beg": "beg", "soilmoisture1": 3263.5206727980826, "bottype": "soil", "soilmoisture2": 3188.218143994256, "soilmoisture3": 2598.6200731506256, "tempc": 30.87949716156633, "battery": 33.57969443411489, "deviceid": "1600aaaaffff0061", "tempf": 80.37714891798022, "volts": 6.966061070410228, "humidity": 19.87654405282617, "CreatedAt": "2018-05-03 12:24:40"}, {"beg": "beg", "soilmoisture1": 3258.3882690682403, "bottype": "soil", "soilmoisture2": 3179.537782652951, "soilmoisture3": 2613.6961426246717, "tempc": 30.89010398880748, "battery": 34.32654840457075, "deviceid": "1600aaaaffff0061", "tempf": 80.35304225593543, "volts": 6.9699332818397135, "humidity": 19.87684083284992, "CreatedAt": "2018-05-03 12:24:52"}];


var colData = [
  { type: 'datetime', label: 'Date' },
  { type: 'number', label: 'Temp' }
];





class EditDataPane extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      json: this.props.data
    }
  }

  callback = (changes) => {
    this.setState({json: changes});
  };

  render() {
    return (
      <div>
        <JsonEditor value={this.state.json} propagateChanges={this.callback} />
      </div>
  )};
}

class DataPane extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      myData: [ ]
    };
  }



  render() {
    let data = this.props.data;
    return (
      <div>
        <h3>Here is where we will put the data</h3>
        <p>JSON - ZZ</p>
        <div>
          <ReactJson src={this.state.myData} collapsed="true"/>
        </div>
      </div>
  )};
}


class Home extends Component {
  render() {

    var graphData = mydata.map(item => [new Date(item.CreatedAt), item.tempf]);



    return (
      <div>
        <h2>Home</h2>
        { /*<MyChart data={graphData} /> */ }
        <hr />
        <BotChart data={graphData} />
        <hr />
        <DataPane data={graphData} />
      </div>
    );
  }
}

export default Home;
