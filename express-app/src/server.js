import express from 'express'
import { fileURLToPath } from 'url'
import { dirname, join } from 'path'
import { router } from './routes/router.js'
import helmet from 'helmet'




/**
 * The main function of the application.
 */
 const main = async () => {
    const app = express();
    const directoryFullName = dirname(fileURLToPath(import.meta.url))
    const buildDir = join(directoryFullName, '..', 'public', 'build')

    // Set various HTTP headers to make the application little more secure (https://www.npmjs.com/package/helmet).
    // (The web application uses external scripts and therefore needs to explicitly trust on code.jquery.com and cdn.jsdelivr.net.)
    // app.use(helmet())
    // app.use(
    //     helmet.contentSecurityPolicy({
    //     directives: {
    //         ...helmet.contentSecurityPolicy.getDefaultDirectives(),
    //         'script-src': ["'self'", 'proxy', 'cdn.jsdelivr.net']
    //     }
    //     })
    // )

    // Parse requests of the content type application/x-www-form-urlencoded.
    // Populates the request object with a body object (req.body).

    // app.use(express.urlencoded({ extended: false }))
    app.set('view engine', 'hbs')
    app.set('views', join(directoryFullName, 'views'))

    app.use(express.static(buildDir))

    app.get('/', function (req, res) {
      res.sendFile(buildDir);
    });


    app.get('/*', router)

     // Error handler.
  app.use(function (err, req, res, next) {
    // 403 Not Found.
    if (err.status === 403) {
      return res
        .status(403)
        .sendFile(join(buildDir, 'errors', '403.html'))
    }
    
    // 404 Not Found.
    if (err.status === 404) {
      return res
        .status(404)
        .sendFile(join(buildDir, 'errors', '404.html'))
    }

    // 500 Internal Server Error (in production, all other errors send this response).
    if (req.app.get('env') !== 'development') {
      return res
        .status(500)
        .sendFile(join(buildDir, 'errors', '500.html'))
    }

    // Development only!
    // Only providing detailed error in development.

    // Render the error page.
    res
      .status(err.status || 500)
      .render('errors/error', { error: err })
  })
    
    app.listen(9000, () => {
        console.log(`Server running`)
        // console.log('Press Ctrl-C to terminate...')
      })
 }

 main().catch(console.error)
