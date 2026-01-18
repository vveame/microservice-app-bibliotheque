const Livre = require("../models/Livre");
const mapper = require("../mappers/LivreMapper");
const { Op } = require("sequelize");

class LivreService {

  async addLivre(data) {
  // Vérifier si un livre avec le même ISBN existe déjà
  const existingLivre = await Livre.findOne({
    where: { isbn: data.isbn }
  });

  if (existingLivre) {
    throw new Error("Un livre avec cet ISBN existe déjà");
  }

  const livre = await Livre.create(mapper.toEntity(data));
  return mapper.toDTO(livre);
}


  async getAllLivres() {
    const livres = await Livre.findAll();
    return livres.map(l => mapper.toDTO(l));
  }

  async getLivreById(id) {
    const livre = await Livre.findByPk(id);
    if (!livre) throw new Error("Livre introuvable");
    return mapper.toDTO(livre);
  }

  async updateLivre(id, data) {
  const livre = await Livre.findByPk(id);
  if (!livre) throw new Error("Livre introuvable");

  // Vérification ISBN seulement si on veut le modifier
  if (data.isbn && data.isbn !== livre.isbn) {
    const existingLivre = await Livre.findOne({
      where: { isbn: data.isbn }
    });

    if (existingLivre) {
      throw new Error("Un autre livre utilise déjà cet ISBN");
    }
  }

  await livre.update(data);
  return mapper.toDTO(livre);
}


  async deleteLivre(id) {
    const livre = await Livre.findByPk(id);
    if (!livre) throw new Error("Livre introuvable");
    await livre.destroy();
  }

  // Recherche par titre / auteur / genre
  async searchLivres(filters) {
    const where = {};

    if (filters.titre) {
      where.titre = { [Op.iLike]: `%${filters.titre}%` };
    }

    if (filters.auteur) {
      where.auteur = { [Op.iLike]: `%${filters.auteur}%` };
    }

    if (filters.genre) {
      where.genre = { [Op.iLike]: `%${filters.genre}%` };
    }

    const livres = await Livre.findAll({ where });
    return livres.map(l => mapper.toDTO(l));
  }

  // Vérifier la disponibilité d’un livre
  async checkDisponibilite(id) {
  const livre = await Livre.findByPk(id);

  if (!livre) {
    throw new Error("Livre introuvable");
  }

  const disponible = livre.numTotalLivres > 0;

  return {
    idLivre: livre.idLivre,
    titre: livre.titre,
    disponible: disponible,
    stock: livre.numTotalLivres
  };
}

}


module.exports = new LivreService();
