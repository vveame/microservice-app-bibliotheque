class RequestLivreDTO {
  constructor({ titre, isbn, auteur, genre, numChapters, numPages, numTotalLivres, image, synopsis  }) {
    this.titre = titre;
    this.isbn = isbn;
    this.auteur = auteur;
    this.genre = genre;
    this.numChapters = numChapters;
    this.numPages = numPages;
    this.numTotalLivres = numTotalLivres;
    this.image = image;       
    this.synopsis = synopsis; 
  }
}

module.exports = RequestLivreDTO;