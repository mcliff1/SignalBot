import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Chart } from 'react-google-charts';



const apiUrl = 'https://1ujflj28sk.execute-api.us-west-2.amazonaws.com/dev/api/metrics/soil?deviceid=1600aaaaffff0061';

const colData = [
  { type: 'datetime', label: 'Date' },
  { type: 'number', label: 'Temp' }
];


class MyChart extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      columns: colData,
      data: this.props.data
    }
  }


  componentWillMount() {
    let currentComponent = this;

    fetch(apiUrl)
    .then( function(resp) {return resp.json(); })
    .then( function(resp_data) {

      var graphData = resp_data.map(item => [new Date(item.CreatedAt), item.tempf]);
      currentComponent.setState({data: graphData});

    });
  }


  render() {
    if (!this.state.data || this.state.data.length === 0 ) return <div>Loading...</div>;
    return (
      <div>
        <Chart chartType="ScatterChart"
               rows={this.state.data}
               columns={this.state.columns}
               options={{}}
               graph_id = "ScatterChart"
               width="100%"
               height="400px"
               legend_toggle
        />
      </div>
    )
  };

}



class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to SignalBot</h1>
        </header>
        <div>   
        <p>My Chart component</p>
        <MyChart />
        </div>
      </div>
    );
  }
}

export default App;
