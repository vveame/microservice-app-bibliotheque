class ResponseLivreDTO {
  constructor(livre) {
    this.idLivre = livre.idLivre;
    this.titre = livre.titre;
    this.isbn = livre.isbn;
    this.auteur = livre.auteur;
    this.genre = livre.genre;
    this.numChapters = livre.numChapters;
    this.numPages = livre.numPages;
    this.numTotalLivres = livre.numTotalLivres;
    this.image = livre.image; // Base64
    this.synopsis = livre.synopsis;
  }
}

module.exports = ResponseLivreDTO;
