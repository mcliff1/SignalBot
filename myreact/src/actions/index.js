/**
 * @file index.js for Action folder
 *
 * Utility methods include
 *
 *  - fetchWithTimeout - wraps fetch with a timeout
 */

export const API_ENDPOINT = 'https://bot-api.mattcliff.net/dev/api/metrics/';


export const fetchWithTimeout = (url, options, delay) => {
  const timer = new Promise((resolve, reject) => {
    setTimeout(() => reject(new Error('timeout at ' + delay)), delay);
  });
  return Promise.race([
      fetch(url, options),
      timer
  ]);
}
