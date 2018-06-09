/**
 * @file chartActions.js
 *
 * All of these actions result in a REDUX event being fired,
 *   the payload or parameters of these actions can be passed
 *   to the redux STORE
 *
 */
import { fetchWithTimeout, API_ENDPOINT } from "./"

const GET_OPTIONS = {
  method: 'GET',
  headers: { 'Content-Type' : 'application/json' }
};

 /**
  * Gets list of device Ids
  */
export const getDeviceIdList = () => ({
  type: 'CHART_LOAD_DEVICEID_LIST',
  payload: fetch(API_ENDPOINT + 'soil?list=true').then(res => res.json()),
});




export const loadData = (deviceid) => {
  const url = API_ENDPOINT + 'soil?deviceid=' + deviceid;

  return({
   type: 'CHART_LOAD_DATA',
   payload: fetchWithTimeout(url, GET_OPTIONS, 5000)
            .then(response => response.json())
 });

   // payload: fetch(API_ENDPOINT + 'soil?deviceid=' + deviceid, {
   //   method: 'GET',
   //   headers: { 'Content-Type' : 'application/json' }
   // }).then(res => res.json())

 }





export const loadDeviceList = () => {
  return ({
    type: 'CHART_DEVICELIST',
    payload: fetch(API_ENDPOINT + 'soil?list=true', {
      method: 'GET',
      headers: { 'Content-Type' : 'application/json' }
    }).then(res => res.json())

  })
}


/**
 * triggers the update of the formatted data from the raw
 */
export const setSource = (source) => {
  return({
    type: 'CHART_SET_DATA',
    source: source,
  });
}
