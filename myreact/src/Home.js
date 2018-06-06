import React, { Component } from 'react';
import ReactJson from 'react-json-view';
import { JsonEditor } from 'react-json-edit';
import { connect } from 'react-redux';




const EditDataPane = ({data, callback}) => {
    return (
      <div className="border">
        <JsonEditor value={data} propagateChanges={(evt) => callback(data)} />
      </div>
  );
};




const DataPane = ({data}) =>  {
    return (
      <div className="border">
        <h3>Here is where we will put the data</h3>
        <p>JSON - Viewer</p>
        <div>
          <ReactJson src={data} collapsed="true"/>
        </div>
      </div>
  );
};


const Home = ({data, callback}) => {
    return (
      <div>
        <h2>Home</h2>
        <p>What are we going to do with this stuff</p>
        <DataPane data={data} />
        <hr />
        <EditDataPane data={data} callback={callback} />
      </div>
    );
  }

const mapStoreToProps = store => {
  return {
    data: store.home.data,
  }
}
const mapDispatchToProps = dispatch => {
  return {
    callback: (evt) => dispatch({
      type: 'JSON_EDIT',
      payload: evt
    })
  }
}


export default connect(mapStoreToProps, mapDispatchToProps)(Home);
