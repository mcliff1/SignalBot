import React from 'react';
import { Chart } from 'react-google-charts';


const ChartView = ({ data, columns }) => (

  <div>
    <Chart chartType="ScatterChart"
               rows={data}
               columns={columns}
               options={{}}
               graph_id = "ScatterChart"
               width="100%"
               height="400px"
               legend_toggle
    />
  </div>
)


export default ChartView;
