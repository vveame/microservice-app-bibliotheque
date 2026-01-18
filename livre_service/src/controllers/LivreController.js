const livreService = require("../services/LivreService");

exports.add = async (req, res, next) => {
  try {
    const data = { ...req.body };

    if (req.file) {
      data.image = req.file.buffer; // ✅ buffer direct
    }

    const result = await livreService.addLivre(data);
    res.status(201).json(result);
  } catch (error) {
    next(error);
  }
};


// 📚 GET ALL
exports.getAll = async (req, res, next) => {
  try {
    const result = await livreService.getAllLivres();
    res.json(result);
  } catch (error) {
    next(error);
  }
};

// 📖 GET BY ID
exports.getById = async (req, res, next) => {
  try {
    const result = await livreService.getLivreById(req.params.id);
    res.json(result);
  } catch (error) {
    next(error);
  }
};

exports.update = async (req, res, next) => {
  try {
    const data = { ...req.body };

    if (req.file) {
      data.image = req.file.buffer;
    }

    const result = await livreService.updateLivre(req.params.id, data);
    res.json(result);
  } catch (error) {
    next(error);
  }
};



// 🗑️ DELETE
exports.delete = async (req, res, next) => {
  try {
    await livreService.deleteLivre(req.params.id);
    res.status(204).end();
  } catch (error) {
    next(error);
  }
};

// 🔍 SEARCH
exports.search = async (req, res, next) => {
  try {
    const result = await livreService.searchLivres(req.query);
    res.json(result);
  } catch (error) {
    next(error);
  }
};

// ✅ DISPONIBILITÉ
exports.checkDisponibilite = async (req, res, next) => {
  try {
    const result = await livreService.checkDisponibilite(req.params.id);
    res.json(result);
  } catch (error) {
    next(error);
  }
};
