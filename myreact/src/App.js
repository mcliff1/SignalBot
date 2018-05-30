import React, { Component } from 'react';
import './App.css';
import ReactJson from 'react-json-view';
import { render } from 'react-dom';
import { Chart } from 'react-google-charts';
import BotChart from './BotChart.js';
import Home from './Home.js';



class App extends Component {
  render() {

    return (
      <div className="App">
        <h2>myreact landing page</h2>
        <hr />
        <Home />
      </div>
    );
  }
}

export default App;
