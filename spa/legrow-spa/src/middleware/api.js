import fetch from 'node-fetch'

const api = async (size) => {

    const response = await fetch(`/api/chart?size=${size}`, {method: 'GET'});

    return response
}

export default api