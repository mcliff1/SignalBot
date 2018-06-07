import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';
import { Nav, Navbar, NavLink, NavItem, NavbarBrand } from 'reactstrap';
import store from './store'
import './App.css';
import Home from './Home';
import MyChart from './MyChart';
import DataView from './DataView';


class App extends Component {
  render() {

    return (
      <Provider store={store}>
      <Router>
      <div>
        <Navbar>
        <NavbarBrand href="/">SignalBot Home</NavbarBrand>
        <Nav navbar>
          <NavItem><NavLink tag={Link} to={'/'}>Home</NavLink></NavItem>
          <NavItem><NavLink tag={Link} to={'/chart'}>Chart</NavLink></NavItem>
          <NavItem><NavLink tag={Link} to={'/data'}>Data</NavLink></NavItem>
        </Nav>
        </Navbar>


        <Switch>
          <Route exact path='/' component={Home} />
          <Route path='/chart' component={MyChart} />
          <Route path='/data' component={DataView} />
        </Switch>
      </div>
      </Router>
      </Provider>
    );
  }
}

export default App;
