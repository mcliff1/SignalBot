import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store'
import './App.css';
import Home from './Home';
import MyChart from './MyChart';


class App extends Component {
  render() {

    return (
      <Provider store={store}>
      <Router>
      <div className="App">
        <h2>SignalBot Home</h2>
        <ul>
        <li><Link to={'/'}>Home</Link></li>
        <li><Link to={'/chart'}>Chart</Link></li>
        </ul>
        <hr />
        <Switch>
          <Route exact path='/' component={Home} />
          <Route path='/chart' component={MyChart} />
        </Switch>
      </div>
      </Router>
      </Provider>
    );
  }
}

export default App;
