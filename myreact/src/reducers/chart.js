/**
 * @file chart.js
 *  Chart Reducer (Redux)
 */
const defaultState = {
  data: null
}

const chart = (state = defaultState, action) => {
  switch (action.type) {
    default:
      console.log('Unhandled Action', action);
      return state;

  }
}


export default chart;
