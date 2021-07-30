import fetch from 'node-fetch'
import fetchChart from '../util/fetcher.js';


/**
 * Main controller.
 *
 */
 export class ApiController {
    /**
     *
     * @param {object} req - Express request object.
     * @param {object} res - Express response object.
     * @param {Function} next - Express next middleware function.
     */
    async getChart(req, res, next) {
        let size = req.query['size']
        const response = await fetchChart(size);
        const body = await response.json();
        
        res.send(body)
    }
  }