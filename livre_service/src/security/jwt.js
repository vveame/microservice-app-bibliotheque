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
    const auth = req.headers["authorization"];

    if (!auth) {
        return res.status(401).json({ error: "Missing Authorization header" });
    }

    const parts = auth.split(" ");
    if (parts.length !== 2 || parts[0] !== "Bearer") {
        return res.status(401).json({ error: "Invalid Authorization header format" });
    }

    const token = parts[1];

    try {
        const payload = jwt.verify(token, PUBLIC_KEY, {
            algorithms: ["RS256"],
            ignoreExpiration: false
        });

        // Attach user info (same idea as Flask g)
        req.user = {
            email: payload.sub,
            roles: payload.scope ? payload.scope.split(" ") : []
        };

        next();
    } catch (err) {
        return res.status(401).json({
            error: "Invalid or expired token",
            message: err.message
        });
    }
}

/**
 * Role-based access control
 */
function rolesRequired(...requiredRoles) {
    return (req, res, next) => {
        if (!req.user || !req.user.roles) {
            return res.status(401).json({ error: "Unauthenticated" });
        }

        const hasRole = requiredRoles.some(role =>
            req.user.roles.includes(role)
        );

        if (!hasRole) {
            return res.status(403).json({
                error: "Forbidden: insufficient role"
            });
        }

        next();
    };
}

module.exports = {
    jwtRequired,
    rolesRequired
};