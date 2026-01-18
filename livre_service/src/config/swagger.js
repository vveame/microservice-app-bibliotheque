const swaggerJSDoc = require("swagger-jsdoc");

const options = {
  definition: {
    openapi: "3.0.0",

    info: {
      title: "Gestion des livres",
      version: "1.0.0",
      description: "API pour la gestion des livres"
    },

    servers: [
      {
        url: "http://localhost:8091"
      }
    ],
    components: {
      schemas: {
        LivreRequest: {
          type: "object",
          required: ["titre", "isbn"],
          properties: {
            titre: { type: "string", example: "Clean Code" },
            isbn: { type: "string", example: "978-0132350884" },
            auteur: { type: "string", example: "Robert C. Martin" },
            genre: { type: "string", example: "Informatique" },
            numChapters: { type: "integer", example: 17 },
            numPages: { type: "integer", example: 464 },
            numTotalLivres: { type: "integer", example: 5 },
            image: { type: "string", example: "https://example.com/cover.jpg" }, 
            synopsis: { type: "string", example: "Résumé du livre..." } 
          }
        },

        LivreResponse: {
          allOf: [
            { $ref: "#/components/schemas/LivreRequest" },
            {
              type: "object",
              properties: {
                idLivre: { type: "integer", example: 1 }
              }
            }
          ]
        },

        ErrorResponse: {
          type: "object",
          properties: {
            message: { type: "string", example: "Livre introuvable" }
          }
        }
      }
    }
  },

  apis: ["./src/routes/*.js"]
};

module.exports = swaggerJSDoc(options);
