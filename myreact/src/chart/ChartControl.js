import React from 'react';
import { Button } from 'reactstrap';


const ChartControl = ({ data, handleLoad, handleSource }) => (
  <div>
    This is my chart control panel,
    <Button onClick={() => handleLoad(document.getElementById('deviceIdText').value)}>Load Data</Button>
    <Button onClick={() => handleSource('BATTERY')}>Battery</Button>
    <Button onClick={() => handleSource('VOLTS')}>Volt</Button>
    <Button onClick={() => handleSource('TEMP')}>Temp</Button>
    <label>Device Id
    <input id='deviceIdText' type="text" defaultValue="1600aaaaffff0061" />
    </label>
    <p> I need to select data to drive the chart and get it into the store</p>
    Here is my Data
    { data ?
      <div className="border">
        {data.map((record, index) => (
          <div key={index}>type {record.type} has label {record.label}</div>
        ))}
      </div>
      :
      <div>No data</div>
    }
  </div>
);



export default ChartControl;
