import React from 'react';
import { Button } from 'reactstrap';


const ChartControl = ({ data, handleLoad, handleSource }) => (
  <div>
    This is my chart control panel,
    <Button onClick={handleLoad}>Load Data</Button>
    <Button onClick={() => handleSource('battery')}>Battery</Button>
    <Button onClick={() => handleSource('volts')}>Volt</Button>
    <Button onClick={() => handleSource('temp')}>Temp</Button>
    <p> I need to select data to drive the chart and get it into the store</p>
    HEre is my Data
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
