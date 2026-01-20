const jwt = require("jsonwebtoken");
const fs = require("fs");
const path = require("path");

// Load RSA public key
const PUBLIC_KEY = fs.readFileSync(
    path.join(__dirname, "../keys/publicKey.pem"),
    "utf8"
);

/**
 * JWT authentication middleware
 */
function jwtRequired(req, res, next) {
    const authHeader = req.headers['authorization'];
    if (!authHeader) return res.status(401).json({ error: 'Missing Authorization header' });

    const parts = authHeader.split(' ');
    if (parts.length !== 2 || parts[0].toLowerCase() !== 'bearer') {
        return res.status(401).json({ error: 'Invalid Authorization header format' });
    }

    const token = parts[1];

    jwt.verify(token, PUBLIC_KEY, { algorithms: ['RS256'] }, (err, payload) => {
        if (err) {
            if (err.name === 'TokenExpiredError') {
                return res.status(401).json({ error: 'Token expired' });
            }
            return res.status(401).json({ error: 'Invalid token', message: err.message });
        }

        // Set user info on request object for later middleware/routes
        req.userId = payload.userId;
        req.userRoles = payload.scope ? payload.scope.split(' ') : [];

        if (!req.userId) {
            return res.status(401).json({ error: 'Invalid token: missing userId' });
        }

        next();
    });
}

// Middleware to check if user has required role(s)
function rolesRequired(...requiredRoles) {
    return (req, res, next) => {
        if (!req.userRoles) {
            return res.status(401).json({ error: 'Missing authentication' });
        }

        const hasRole = requiredRoles.some(role => req.userRoles.includes(role));
        if (!hasRole) {
            return res.status(403).json({ error: 'Access forbidden: insufficient role' });
        }

        next();
    };
}

module.exports = {
    jwtRequired,
    rolesRequired
};