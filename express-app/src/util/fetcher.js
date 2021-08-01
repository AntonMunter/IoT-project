import fetch from 'node-fetch'

const fetchChart = async (size) => {

    const response = await fetch(`http://flask:5000/api/data?size=${size}`, {method: 'GET'});
    return response
}

export default fetchChart