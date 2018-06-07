/**
 * @file store.js
 *  creates the redux store
 */
import { createStore, applyMiddleware } from 'redux';
import promiseMiddleware from 'redux-promise-middleware';
import thunkMiddleware from 'redux-thunk';
import logger from 'redux-logger';
import reducer from './reducers';

const middleware = applyMiddleware(thunkMiddleware, promiseMiddleware(), logger);
const store = createStore(reducer, {}, middleware);

export default store;
