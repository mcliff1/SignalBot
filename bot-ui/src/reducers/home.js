/**
 * @file home.js
 *  Home Reducer (Redux)
 */


 const mydata = [
   { deviceid : 'bot1', CreatedAt: '2018-04-30 12:23:34', temp: 76.2, humidity: 26.1 },
   { deviceid : 'bot2', CreatedAt: '2018-05-02 12:23:34', temp: 76.4, humidity: 26.0 },
   { deviceid : 'bot3', CreatedAt: '2018-05-05 12:23:34', temp: 76.6, humidity: 26.0 },
 ];


const defaultState = {
  data: mydata,
}


const home = (state = defaultState, action) => {

  switch(action.type) {
    case 'JSON_EDIT':
      return {
        data: action.payload,
        ...state
      }
    default:
      return state;

  }
}


export default home;
