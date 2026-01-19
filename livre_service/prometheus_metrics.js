const client = require('prom-client');

// Create metrics
const httpRequestDurationSeconds = new client.Histogram({
    name: 'node_http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'code'],
    buckets: [0.1, 0.5, 1, 1.5, 2, 5]
});

const httpRequestsTotal = new client.Counter({
    name: 'node_http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'code']
});

// Middleware to collect metrics safely
function metricsMiddleware(req, res, next) {
    try {
        const end = httpRequestDurationSeconds.startTimer();

        res.on('finish', () => {
            try {
                const routePath = req.route ? req.route.path : req.path || 'unknown';
                const method = req.method || 'unknown';
                const statusCode = res.statusCode ? res.statusCode.toString() : 'unknown';

                httpRequestsTotal.inc({ method, route: routePath, code: statusCode });
                end({ method, route: routePath, code: statusCode });
            } catch (err) {
                console.error('Error recording metrics:', err);
            }
        });

        next();
    } catch (err) {
        console.error('Error in metrics middleware:', err);
        next();
    }
}

// Metrics endpoint handler safely
async function metricsEndpoint(req, res) {
    try {
        res.set('Content-Type', client.register.contentType);
        res.end(await client.register.metrics());
    } catch (err) {
        console.error('Error generating metrics:', err);
        res.status(500).send('Error generating metrics');
    }
}

module.exports = {
    metricsMiddleware,
    metricsEndpoint
};