const ResponseLivreDTO = require("../dto/ResponseLivreDTO");

module.exports = {
  toEntity(dto) {
    return { ...dto };
  },

  toDTO(livre) {
    return new ResponseLivreDTO({
      ...livre.dataValues,
      image: livre.image
        ? `data:image/jpeg;base64,${livre.image.toString("base64")}`
        : null
    });
  }
};
