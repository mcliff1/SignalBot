import React, { Component } from 'react';
import ReactJson from 'react-json-view';
import { JsonEditor } from 'react-json-edit';


const mydata = [
  { deviceid : 'bot2', CreatedAt: '2018-04-30 12:23:34', temp: 76.2, humidity: 26.1 },
  { deviceid : 'bot2', CreatedAt: '2018-05-02 12:23:34', temp: 76.4, humidity: 26.0 },
  { deviceid : 'bot2', CreatedAt: '2018-05-05 12:23:34', temp: 76.6, humidity: 26.0 },
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

    return (
      <div>
        <h2>Home</h2>
        <p>What are we going to do with this stuff</p>
        <DataPane />
        <hr />
        <EditDataPane />
      </div>
    );
  }
}

export default Home;
