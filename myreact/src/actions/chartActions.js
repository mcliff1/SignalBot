/**
 * @file chartActions.js
 *
 * All of these actions result in a REDUX event being fired,
 *   the payload or parameters of these actions can be passed
 *   to the redux STORE
 *
 */
 const API_ENDPOINT = 'https://bot-api.mattcliff.net/dev/api/metrics/';

 const mydata = [
 {"beg": "beg", "soilmoisture1": 3274.1247255622106, "bottype": "soil", "soilmoisture2": 3175.1096242331837, "soilmoisture3": 2578.5454259691796, "tempc": 30.796327555154228, "battery": 33.427733389278316, "deviceid": "1600aaaaffff0061", "tempf": 80.5677449690722, "volts": 6.954768988153674, "humidity": 19.892216299843522, "CreatedAt": "2018-05-03 12:23:34"}, {"beg": "beg", "soilmoisture1": 3267.938623417472, "bottype": "soil", "soilmoisture2": 3173.7498416365506, "soilmoisture3": 2578.8472637141294, "tempc": 30.79168747795165, "battery": 32.72386002291308, "deviceid": "1600aaaaffff0061", "tempf": 80.5070478174702, "volts": 6.97322181626109, "humidity": 19.882237496321714, "CreatedAt": "2018-05-03 12:23:48"}, {"beg": "beg", "soilmoisture1": 3269.604807068043, "bottype": "soil", "soilmoisture2": 3180.7115081231445, "soilmoisture3": 2579.8048316696627, "tempc": 30.91349889600696, "battery": 32.91031186709302, "deviceid": "1600aaaaffff0061", "tempf": 80.35202682014672, "volts": 6.970779553140899, "humidity": 19.895292757506102, "CreatedAt": "2018-05-03 12:24:00"}, {"beg": "beg", "soilmoisture1": 3268.1887284868158, "bottype": "soil", "soilmoisture2": 3179.766829020895, "soilmoisture3": 2588.692646573567, "tempc": 30.819158521188392, "battery": 33.60084482516983, "deviceid": "1600aaaaffff0061", "tempf": 80.27986394451564, "volts": 6.971174577661359, "humidity": 19.889563807490713, "CreatedAt": "2018-05-03 12:24:13"}, {"beg": "beg", "soilmoisture1": 3256.874787909703, "bottype": "soil", "soilmoisture2": 3183.3744875370044, "soilmoisture3": 2586.986083832782, "tempc": 30.805541967720135, "battery": 33.83118630220724, "deviceid": "1600aaaaffff0061", "tempf": 80.43475613213707, "volts": 6.965575978924227, "humidity": 19.887207789776546, "CreatedAt": "2018-05-03 12:24:27"}, {"beg": "beg", "soilmoisture1": 3263.5206727980826, "bottype": "soil", "soilmoisture2": 3188.218143994256, "soilmoisture3": 2598.6200731506256, "tempc": 30.87949716156633, "battery": 33.57969443411489, "deviceid": "1600aaaaffff0061", "tempf": 80.37714891798022, "volts": 6.966061070410228, "humidity": 19.87654405282617, "CreatedAt": "2018-05-03 12:24:40"}, {"beg": "beg", "soilmoisture1": 3258.3882690682403, "bottype": "soil", "soilmoisture2": 3179.537782652951, "soilmoisture3": 2613.6961426246717, "tempc": 30.89010398880748, "battery": 34.32654840457075, "deviceid": "1600aaaaffff0061", "tempf": 80.35304225593543, "volts": 6.9699332818397135, "humidity": 19.87684083284992, "CreatedAt": "2018-05-03 12:24:52"}];


 /**
  * Gets list of device Ids
  */
 export const getDeviceIdList = ({deviceid}) => ({
   type: 'CHART_LOAD_DEVICEID_LIST',

    payload: fetch(API_ENDPOINT+'soil?list=true', {
      method: 'GET',
      headers: { 'Content-Type' : 'application/json' }
    }).then(res => res.json())

  });


/**
 * Returns live Data
 */
export const loadData2 = ({deviceid}) => ({
  type: 'CHART_LOAD_DATA',
  payload: new Promise(resolve => {
    setTimeout(() => {
      fetch(API_ENDPOINT + 'soil?deviceid=' + deviceid,
        {
          method: 'GET',
          headers: {'Content-Type' : 'application/json'}
        }).then(res => res.json());
      }, 2000);
   })

  // payload: fetch(API_ENDPOINT + 'soil?deviceid=' + deviceid, {
  //   method: 'GET',
  //   headers: { 'Content-Type' : 'application/json' }
  // }).then(res => res.json())

 });


 export const loadData = ({deviceid}) => ({
   type: 'CHART_LOAD_DATA',
   payload: new Promise(resolve => {
     setTimeout(() => {
       fetch(API_ENDPOINT + 'soil?deviceid=' + deviceid,
         {
           method: 'GET',
           headers: {'Content-Type' : 'application/json'}
         }).then(response => response.json());
       }, 2000);
    })

   // payload: fetch(API_ENDPOINT + 'soil?deviceid=' + deviceid, {
   //   method: 'GET',
   //   headers: { 'Content-Type' : 'application/json' }
   // }).then(res => res.json())

  });



 /**
  * Returns canned Data
  */
 export const loadCannedData = () => {
   return({
     type: 'CHART_LOAD_DATA',
     payload: mydata
   });
 }


// utility to get column
const getColumnData = (source) => {
  return [
    { type: 'datetime', label: 'Date' },
    { type: 'number', label: source }
  ]
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
  export const setSource = (source, rawData) => {

    switch(source) {
      case 'TEMP':
        return({
          type: 'CHART_SET_DATA',
          column_data: getColumnData(source),
          row_data: rawData.map(item => [new Date(item.CreatedAt), item.tempf])
        });
      case 'VOLTS':
        return({
          type: 'CHART_SET_DATA',
          column_data: getColumnData(source),
          row_data: rawData.map(item => [new Date(item.CreatedAt), item.volts])
        });
      case 'BATTERY':
        return({
          type: 'CHART_SET_DATA',
          column_data: getColumnData(source),
          row_data: rawData.map(item => [new Date(item.CreatedAt), item.battery])
        });

      default:
        console.log('unknown source type', source);
        return({ type: 'NO_OP' });
    }


  }
