module.exports = (err, req, res, next) => {
  console.error(err);
  // ISBN déjà existant
  if (err.message.includes("ISBN")) {
    return res.status(409).json({
      message: err.message
    });
  }

  // Livre introuvable
  if (err.message.includes("introuvable")) {
    return res.status(404).json({
      message: err.message
    });
  }

  // Erreur serveur (par défaut)
  return res.status(500).json({
    message: "Erreur serveur"
  });
};
