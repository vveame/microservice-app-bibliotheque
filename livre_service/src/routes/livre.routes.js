const express = require("express");
const controller = require("../controllers/LivreController");
const multer = require("multer");
const { jwtRequired, rolesRequired } = require("../security/jwt");

const router = express.Router();


const upload = multer();

/**
 * @swagger
 * tags:
 *   name: Livres
 *   description: Gestion des livres
 */


/**
 * @swagger
 * /v1/livres:
 *   post:
 *     summary: Ajouter un nouveau livre
 *     tags: [Livres]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/LivreRequest'
 *     responses:
 *       201:
 *         description: Livre ajouté avec succès
 *       409:
 *         description: ISBN déjà existant
 *       500:
 *         description: Erreur serveur
 */

// ROUTES
router.post("/",
    jwtRequired,
    rolesRequired("ROLE_BIBLIOTHECAIRE"),
    upload.single("image"),
    controller.add);

/**
 * @swagger
 * /v1/livres/{id}:
 *   put:
 *     summary: Modifier un livre
 *     tags: [Livres]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/LivreRequest'
 *     responses:
 *       200:
 *         description: Livre modifié
 *       409:
 *         description: ISBN déjà utilisé
 */
router.put("/:id",
    jwtRequired,
    rolesRequired("ROLE_BIBLIOTHECAIRE"),
    upload.single("image"),
    controller.update);

/**
 * @swagger
 * /v1/livres/{id}:
 *   delete:
 *     summary: Supprimer un livre
 *     tags: [Livres]
 *     responses:
 *       204:
 *         description: Livre supprimé
 */
router.delete("/:id",
    jwtRequired,
    rolesRequired("ROLE_BIBLIOTHECAIRE"),
    controller.delete);

/**
 * @swagger
 * /v1/livres:
 *   get:
 *     summary: Récupérer tous les livres
 *     tags: [Livres]
 *     responses:
 *       200:
 *         description: Liste des livres
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/LivreResponse'
 */
router.get("/", controller.getAll);

/**
 * @swagger
 * /v1/livres/search:
 *   get:
 *     summary: Recherche de livres (titre, auteur, genre)
 *     tags: [Livres]
 *     parameters:
 *       - in: query
 *         name: titre
 *         schema:
 *           type: string
 *       - in: query
 *         name: auteur
 *         schema:
 *           type: string
 *       - in: query
 *         name: genre
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Résultat de la recherche
 */
router.get("/search", controller.search);

/**
 * @swagger
 * /v1/livres/{id}/disponibilite:
 *   get:
 *     summary: Vérifier la disponibilité d’un livre
 *     tags: [Livres]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *     responses:
 *       200:
 *         description: Disponibilité du livre
 *       404:
 *         description: Livre introuvable
 */
router.get("/:id/disponibilite", controller.checkDisponibilite);

/**
 * @swagger
 * /v1/livres/{id}:
 *   get:
 *     summary: Récupérer un livre par ID
 *     tags: [Livres]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Livre trouvé
 *       404:
 *         description: Livre introuvable
 */
router.get("/:id", controller.getById);

module.exports = router;
