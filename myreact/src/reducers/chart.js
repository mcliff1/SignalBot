/**
 * @file chart.js
 *  Chart Reducer (Redux)
 */
const defaultState = {
  rawData: null,
  data: null,
  columns: null
}

const chart = (state = defaultState, action) => {
  switch (action.type) {
    case 'CHART_LOAD_DATA_FULFILLED':
      return {
        ...state,
        rawData: action.payload,
      };

    case 'CHART_SET_DATA':
      return {
        ...state,
        data: action.row_data,
        columns: action.column_data
      };

    default:
      console.log('Unhandled Action', action.type);
      return state;

  }
}


export default chart;
