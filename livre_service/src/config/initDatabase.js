const { Client } = require("pg");
require("dotenv").config();

async function initDatabase() {
  const client = new Client({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: "postgres" // base par défaut
  });

  try {
    await client.connect();

    const res = await client.query(
      "SELECT 1 FROM pg_database WHERE datname = $1",
      [process.env.DB_NAME]
    );

    if (res.rowCount === 0) {
      await client.query(`CREATE DATABASE "${process.env.DB_NAME}"`);
      console.log(`✅ Base de données '${process.env.DB_NAME}' créée`);
    } else {
      console.log(`ℹ️ Base de données '${process.env.DB_NAME}' existe déjà`);
    }

  } catch (err) {
    console.error("❌ Erreur création DB :", err.message);
    throw err;
  } finally {
    await client.end();
  }
}

module.exports = initDatabase;
