const axios = require("axios");
const os = require("os");

const EUREKA_SERVER =
    (process.env.EUREKA_SERVER || "http://localhost:8761/eureka").replace(/\/$/, "");

const APP_NAME = process.env.APP_NAME || "LIVRE-SERVICE";
const PORT = process.env.PORT || 8080;

const HOSTNAME = os.hostname();

// Get local IP (better than 127.0.0.1)
function getIpAddress() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === "IPv4" && !iface.internal) {
                return iface.address;
            }
        }
    }
    return "127.0.0.1";
}

const IP_ADDR = getIpAddress();
const INSTANCE_ID = `${HOSTNAME}:${APP_NAME}:${PORT}`;

const registrationPayload = {
    instance: {
        instanceId: INSTANCE_ID,        // e.g. 'hostname:APP_NAME:PORT'
        app: APP_NAME.toUpperCase(),   // APP_NAME in uppercase
        hostName: IP_ADDR,             // IP address string
        ipAddr: IP_ADDR,               // IP address string
        vipAddress: APP_NAME.toLowerCase(),        // APP_NAME in lowercase
        secureVipAddress: APP_NAME.toLowerCase(),  // APP_NAME in lowercase
        status: "UP",
        port: {
            $: PORT,          // port number as number (or string)
            "@enabled": "true"
        },
        healthCheckUrl: `http://${IP_ADDR}:${PORT}/actuator/health`,
        statusPageUrl: `http://${IP_ADDR}:${PORT}/actuator/health`,
        homePageUrl: `http://${IP_ADDR}:${PORT}/`,
        metadata: {
            "management.port": PORT.toString()
        },
        dataCenterInfo: {
            "@class": "com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo",
            name: "MyOwn"
        }
    }
};

async function registerToEureka() {
    const url = `${EUREKA_SERVER}/apps/${APP_NAME}`;
    try {
        console.log("Registering to Eureka:", url);
        const res = await axios.post(url, registrationPayload, {
            headers: { "Content-Type": "application/json" }
        });
        console.log("Registered to Eureka:", res.status);
    } catch (err) {
        console.error(
            "Eureka registration failed:",
            err.response?.status,
            err.response?.data || err.message
        );
    }
}

async function sendHeartbeat() {
    const url = `${EUREKA_SERVER}/apps/${APP_NAME}/${INSTANCE_ID}`;
    try {
        await axios.put(url);
        console.log("Eureka heartbeat OK");
    } catch (err) {
        console.warn("Eureka heartbeat failed");
    }
}

async function deregisterFromEureka() {
    const url = `${EUREKA_SERVER}/apps/${APP_NAME}/${INSTANCE_ID}`;
    try {
        await axios.delete(url);
        console.log("Deregistered from Eureka");
    } catch (err) {
        console.warn("Eureka deregistration failed");
    }
}

function startEurekaClient() {
    registerToEureka();

    const heartbeatInterval = setInterval(sendHeartbeat, 30_000);

    const shutdown = async () => {
        console.log("Shutting down, deregistering from Eureka...");
        clearInterval(heartbeatInterval);
        await deregisterFromEureka();
        process.exit(0);
    };

    process.on("SIGINT", shutdown);
    process.on("SIGTERM", shutdown);
}

module.exports = {
    startEurekaClient
};
