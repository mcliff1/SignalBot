import React from 'react';
import { Button } from 'reactstrap';


const ChartControl = ({ data, deviceIdList, handleLoad, handleSource }) => {

  const handleDeviceIdChange = () => {
    //const val = e.selectedIndex;
    //alert('handle' + e);
    const x = document.getElementById('myDiD');
    const deviceId = x.options[x.selectedIndex].value;
    handleLoad(deviceId);
  }

  return(
  <div>
    This is my chart control panel,
    <Button onClick={() => {
      const x = document.getElementById('myDiD');
      //handleLoad(document.getElementById('deviceId').value)}
    }}>Load Data</Button>
    <Button onClick={() => handleSource('battery')}>Battery</Button>
    <Button onClick={() => handleSource('volts')}>Volt</Button>
    <Button onClick={() => handleSource('tempf')}>Temp</Button>
    <label>Device Id
    <select id='myDiD' onChange={handleDeviceIdChange}>
      {deviceIdList.map((id, index) =>
        <option key={index} value={id}>{id}</option>
      )}
    </select>
    </label>
    <p> I need to select data to drive the chart and get it into the store</p>
    { data ?
      <div className="border">
        There are {data.length} records loaded
      </div>
      :
      <div>No data present</div>
    }
  </div>
);
}

export default ChartControl;
