package prete_service.web;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;
import prete_service.DTO.RequestPreteDTO;
import prete_service.DTO.ResponsePreteDTO;
import prete_service.service.PreteServiceImpl;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

@OpenAPIDefinition(
        info = @Info(
                title= "Gestion des prêts",
                description= "offre tous les methodes pour gérer les prêts de livres",
                version= "1.0.0"
        ),
        servers = @Server(
                url = "http://localhost:8092/"
        )
)
@RestController
@RequestMapping("/v1/pretes")
public class ApiRestfull {

    private final PreteServiceImpl preteService;

    public ApiRestfull(PreteServiceImpl preteService) {
        this.preteService = preteService;
    }

    // Ajouter un prêt
    @Operation(
            summary = "Ajouter un prêt",
            description = "Permet d’ajouter un nouveau prêt.",
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    content = @Content(
                            mediaType = "application/json",
                            schema = @Schema(implementation = RequestPreteDTO.class)
                    )
            ),
            responses = {
                    @ApiResponse(responseCode = "200", description = "Prêt ajouté avec succès",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = ResponsePreteDTO.class))),
                    @ApiResponse(responseCode = "400", description = "Erreur côté client"),
                    @ApiResponse(responseCode = "500", description = "Erreur côté serveur")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @PostMapping
    public ResponseEntity<ResponsePreteDTO> addPrete(@RequestBody RequestPreteDTO requestPreteDTO) {
        ResponsePreteDTO responsePreteDTO = preteService.addPrete(requestPreteDTO);
        return ResponseEntity.ok(responsePreteDTO);
    }

    // Mettre à jour un prêt
    @Operation(
            summary = "Mettre à jour un prêt",
            description = "Permet de modifier les informations d’un prêt existant.",
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    required = true,
                    content = @Content(
                            mediaType = "application/json",
                            schema = @Schema(implementation = RequestPreteDTO.class)
                    )
            ),
            responses = {
                    @ApiResponse(responseCode = "200", description = "Prêt mis à jour avec succès",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = ResponsePreteDTO.class))),
                    @ApiResponse(responseCode = "404", description = "Prêt introuvable"),
                    @ApiResponse(responseCode = "500", description = "Erreur côté serveur")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @PutMapping("/{id}")
    public ResponseEntity<ResponsePreteDTO> updatePrete(@PathVariable int id, @RequestBody RequestPreteDTO requestPreteDTO) {
        ResponsePreteDTO responsePreteDTO = preteService.updatePrete(id, requestPreteDTO);
        return ResponseEntity.ok(responsePreteDTO);
    }

    // Récupérer tous les prêts
    @Operation(
            summary = "Afficher tous les prêts",
            description = "Retourne la liste complète des prêts.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Liste récupérée avec succès",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = ResponsePreteDTO.class)))
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @GetMapping
    public ResponseEntity<List<ResponsePreteDTO>> getAllPretes() {
        List<ResponsePreteDTO> responsePreteDTOS = preteService.getAllPretes();
        return ResponseEntity.ok(responsePreteDTOS);
    }

    // Récupérer un prêt par ID
    @Operation(
            summary = "Récupérer un prêt par ID",
            parameters = @Parameter(name = "id", required = true),
            description = "Retourne les informations d’un prêt spécifique.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Prêt trouvé avec succès",
                            content = @Content(mediaType = "application/json",
                                    schema = @Schema(implementation = ResponsePreteDTO.class))),
                    @ApiResponse(responseCode = "404", description = "Prêt introuvable"),
                    @ApiResponse(responseCode = "500", description = "Erreur côté serveur")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @GetMapping("/{id}")
    public ResponseEntity<ResponsePreteDTO> getPreteById(@PathVariable Integer id) {
        ResponsePreteDTO responsePreteDTO = preteService.getPreteById(id);
        return ResponseEntity.ok(responsePreteDTO);
    }

    // Supprimer un prêt par ID
    @Operation(
            summary = "Supprimer un prêt",
            description = "Supprime un prêt de la base de données selon son identifiant.",
            responses = {
                    @ApiResponse(responseCode = "200", description = "Prêt supprimé avec succès"),
                    @ApiResponse(responseCode = "404", description = "Prêt introuvable"),
                    @ApiResponse(responseCode = "500", description = "Erreur côté serveur")
            }
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePrete(@PathVariable Integer id) {
        preteService.deletePrete(id);
        return ResponseEntity.ok().build();
    }


    @Operation(
            summary = "Retourner un livre",
            description = "Marque un livre comme retourné (livreRetourne = true)."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @PutMapping("/{id}/retourner")
    public ResponseEntity<ResponsePreteDTO> retournerLivre(@PathVariable Integer id) {
        ResponsePreteDTO responsePreteDTO = preteService.retournerLivre(id);
        return ResponseEntity.ok(responsePreteDTO);
    }

    @Operation(
            summary = "Prolonger un prêt",
            description = "Prolonge la date de fin d'un prêt."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @PutMapping("/{id}/prolonger")
    public ResponseEntity<ResponsePreteDTO> extendPrete(
            @PathVariable Integer id,
            @RequestParam @DateTimeFormat(pattern = "yyyy-MM-dd") Date newDateFinPret) {
        ResponsePreteDTO responsePreteDTO = preteService.extendPrete(id, newDateFinPret);
        return ResponseEntity.ok(responsePreteDTO);
    }

    @Operation(
            summary = "Lister les anciens prêts",
            description = "Retourne la liste des prêts où le livre a été retourné."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @GetMapping("/anciennes")
    public ResponseEntity<List<ResponsePreteDTO>> anciennePrete() {
        List<ResponsePreteDTO> responsePreteDTOS = preteService.anciennePrete();
        return ResponseEntity.ok(responsePreteDTOS);
    }

    @Operation(
            summary = "Lister les prêts actifs",
            description = "Retourne la liste des prêts actifs (non retournés et non expirés)."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @GetMapping("/actifs")
    public ResponseEntity<List<ResponsePreteDTO>> preteActif() {
        List<ResponsePreteDTO> responsePreteDTOS = preteService.preteActif();
        return ResponseEntity.ok(responsePreteDTOS);
    }

    @Operation(
            summary = "Lister les prêts en retard",
            description = "Retourne la liste des prêts en retard (date de fin dépassée)."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @GetMapping("/retards")
    public ResponseEntity<List<ResponsePreteDTO>> retardPrete() {
        List<ResponsePreteDTO> responsePreteDTOS = preteService.retardPrete();
        return ResponseEntity.ok(responsePreteDTOS);
    }

    @Operation(
            summary = "Créer une demande de prêt",
            description = "Crée une demande de prêt (demande = true)."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_LECTEUR')")
    @PostMapping("/demandes")
    public ResponseEntity<ResponsePreteDTO> demandePrete(@RequestBody RequestPreteDTO requestPreteDTO) {
        ResponsePreteDTO responsePreteDTO = preteService.demandePrete(requestPreteDTO);
        return ResponseEntity.ok(responsePreteDTO);
    }

    @Operation(
            summary = "Rejeter une demande de prêt",
            description = "Supprime une demande de prêt."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @DeleteMapping("/demandes/{id}/rejeter")
    public ResponseEntity<Void> rejeterPrete(@PathVariable Integer id) {
        preteService.rejeterPrete(id);
        return ResponseEntity.ok().build();
    }

    @Operation(
            summary = "Accepter une demande de prêt",
            description = "Convertit une demande de prêt en prêt actif."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @PutMapping("/demandes/{id}/accepter")
    public ResponseEntity<ResponsePreteDTO> accepterPrete(@PathVariable Integer id) {
        ResponsePreteDTO responsePreteDTO = preteService.accepterPrete(id);
        return ResponseEntity.ok(responsePreteDTO);
    }

    @Operation(
            summary = "Lister toutes les demandes de prêt",
            description = "Retourne la liste de toutes les demandes de prêt (demande = true)."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_BIBLIOTHECAIRE')")
    @GetMapping("/demandes")
    public ResponseEntity<List<ResponsePreteDTO>> getAllDemandes() {
        List<ResponsePreteDTO> responsePreteDTOS = preteService.getAllDemandes();
        return ResponseEntity.ok(responsePreteDTOS);
    }

    //for the ML in the future if needed
    @Operation(
            summary = "Lister uniquement les prêts réels",
            description = "Retourne uniquement les prêts réels (demande = false). " +
                    "Utile pour les systèmes de recommandation ML."
    )
    @GetMapping("/pretesonly")
    public ResponseEntity<List<ResponsePreteDTO>> getPretesOnly() {
        List<ResponsePreteDTO> responsePreteDTOS = preteService.getPretesOnly();
        return ResponseEntity.ok(responsePreteDTOS);
    }

    @Operation(
            summary = "Historique des prêts d'un utilisateur",
            description = "Retourne tous les prêts réels (demande = false) d'un utilisateur spécifique, triés du plus récent au plus ancien."
    )
    @PreAuthorize("hasAuthority('SCOPE_ROLE_LECTEUR')")
    @GetMapping("/lecteurs/{idLecteur}/historique")
    public ResponseEntity<List<ResponsePreteDTO>> getUserLoanHistory(@PathVariable String idLecteur) {
        List<ResponsePreteDTO> history = preteService.getUserLoanHistory(idLecteur);
        return ResponseEntity.ok(history);
    }
}
