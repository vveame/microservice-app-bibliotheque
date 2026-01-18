const express = require("express");
const sequelize = require("./src/config/database");
const livreRoutes = require("./src/routes/livre.routes");
const swaggerUi = require("swagger-ui-express");
const swaggerSpec = require("./src/config/swagger");
const initDatabase = require("./src/config/initDatabase");
require("dotenv").config();
const { startEurekaClient } = require("./eureka_client");

const app = express();

// Middlewares
app.use(express.json());

//Eureka health check
app.get("/health", (req, res) => {
    res.json({ status: "UP" });
});

// Routes
app.use("/swagger", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.use("/v1/livres", livreRoutes);

// 404
app.use((req, res) => {
  res.status(404).json({
    message: "Route non trouvée"
  });
});

// Error handler
app.use(require("./src/middlewares/errorHandler"));

// 🚀 DÉMARRAGE AUTOMATIQUE
(async () => {
  try {
    // 1️⃣ Créer la base si elle n’existe pas
    await initDatabase();

    // 2️⃣ Synchroniser les tables
    await sequelize.sync({ alter: true });
    console.log("Base PostgreSQL connectée");

    // 3️⃣ Lancer le serveur
    app.listen(process.env.PORT, () => {
      console.log(`Service Livre lancé sur ${process.env.PORT}`);

        // START EUREKA HERE
        startEurekaClient();
    });

  } catch (error) {
    console.error("❌ Échec du démarrage :", error.message);
    process.exit(1);
  }
})();
