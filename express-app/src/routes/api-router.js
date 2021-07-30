import express from 'express'
import { ApiController } from '../controllers/api-controller.js'

export const router = express.Router()

const apiController = new ApiController()

router.get('/chart?', (req, res, next) => apiController.getChart(req, res, next))

router.use('*', (req, res, next) => next(createError(404)))

