const { DataTypes } = require("sequelize");
const sequelize = require("../config/database");

const Livre = sequelize.define("Livre", {
  idLivre: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  titre: {
    type: DataTypes.STRING,
    allowNull: false
  },
  isbn: {
    type: DataTypes.STRING,
    unique: true 
  },
  auteur: {
    type: DataTypes.STRING
  },
  genre: {
    type: DataTypes.STRING
  },
  numChapters: {
    type: DataTypes.INTEGER
  },
  numPages: {
    type: DataTypes.INTEGER
  },
  numTotalLivres: {
    type: DataTypes.INTEGER
  },
   image: {
  type: DataTypes.BLOB // BYTEA en PostgreSQL
},
  synopsis: {                 
    type: DataTypes.TEXT
  }
});

module.exports = Livre;
