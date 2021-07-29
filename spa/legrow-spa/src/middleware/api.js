import fetch from 'node-fetch'
import dotenv from "dotenv";
dotenv.config({ silent: process.env.NODE_ENV === 'dev' });

const api = async (size) => {
    const meta = {
        'Auth': process.env.REACT_APP_API_TOKEN
      };

      const headers = new Headers(meta);

    const response = await fetch(`http://13.51.17.114:5000/api/data?size=${size}`, {method: 'GET', headers: headers});
    // const body = await response.text();
    return response
}

export default api