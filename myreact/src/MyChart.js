import React from 'react';
import { connect } from 'react-redux';
import ChartView from './chart/ChartView';
import ChartControl from './chart/ChartControl'
import { loadData, setSource, getDeviceIdList } from './actions/chartActions';

const MyChart = ( {rawData, data, deviceIdList, columns, setSource, loadData } ) => {


  // this packs the rawData property onto the setSource method to dispatch
  const setSourceWithData = (source) => {
    return setSource(source, rawData);
  }

    return (
      <div>
        <ChartControl
            data={rawData}
            deviceIdList={deviceIdList}
            handleLoad={loadData}
            handleSource={setSourceWithData} />
        { /*<MyChart data={graphData} /> */ }
        <hr />
        {
          data && (data.length > 0) ?
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
    columns: store.chart.columns,
    deviceIdList: store.chart.deviceIdList
  }
}

const mapDispathToProps = (dispatch, ownProps) => {
  return {
    loadData: (deviceid) => dispatch(loadData(deviceid)),
    setSource: (source, data) => dispatch(setSource(source, data)),
    getDeviceIdList: () => dispatch(getDeviceIdList())
  }
}

export default connect(mapStoreToProps, mapDispathToProps)(MyChart);
