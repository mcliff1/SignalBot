import React from 'react';
import { connect } from 'react-redux';
import ChartView from './chart/ChartView';
import ChartControl from './chart/ChartControl'
import { loadData, setSource } from './actions/chartActions';

const MyChart = ( {rawData, data, columns, setSource, loadData } ) => {

  const setSource2 = (source) => {
    console.log('in there');
    return setSource(source, rawData);
  }

    return (
      <div>
        <ChartControl data={columns}
            handleLoad={loadData}
            handleSource={setSource2} />
        { /*<MyChart data={graphData} /> */ }
        <hr />
        {
          data ?
          <ChartView data={data} columns={columns} />
          : <div>No data</div>
        }
        <hr />
      </div>
    );
  }


// from reduxjs.org/basics/usage-with-react
//  maps from the overall store to this component props
const mapStoreToProps = store => {
  return {
    rawData: store.chart.rawData,
    data: store.chart.data,
    columns: store.chart.columns
  }
}

const mapDispathToProps = (dispatch, ownProps) => {
  console.log('ownProps', ownProps);
  return {
    loadData: () => dispatch(loadData()),
    setSource: (source, data) => dispatch(setSource(source, data))
  }
}

export default connect(mapStoreToProps, mapDispathToProps)(MyChart);
