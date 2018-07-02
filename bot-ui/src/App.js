import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link, Switch } from 'react-router-dom';
import { connect } from 'react-redux';
import { Nav, Navbar, NavLink, NavItem, NavbarBrand } from 'reactstrap';
import './App.css';
import Home from './Home';
import Menu, { MenuItem } from 'rc-menu';
import MyChart from './MyChart';
import DataView from './DataView';
import { loadDeviceList } from './actions/chartActions';


class App extends Component {

  componentWillMount() {
    this.props.loadDeviceList();
  }

  render() {

    return (
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
        <Menu>
        <MenuItem>Home</MenuItem>
        </Menu>


        <Switch>
          <Route exact path='/' component={Home} />
          <Route path='/chart' component={MyChart} />
          <Route path='/data' component={DataView} />
        </Switch>
      </div>
      </Router>
    );
  }
}

const mapStateToProps = (state) => {
  return {
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    loadDeviceList: () => dispatch(loadDeviceList()),
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(App);
