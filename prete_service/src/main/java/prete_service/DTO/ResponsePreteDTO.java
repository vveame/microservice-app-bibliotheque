package prete_service.DTO;

import lombok.*;
import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class ResponsePreteDTO {
    private Integer idPret;
    private String titre;
    private String description;
    private Date datePret;
    private Date dateFinPret;
    private Boolean livreRetourne;
    private Boolean demande;
    private String idLecteur;
    private Integer idLivre;
    private Livre livre;
    private Lecteur lecteur;
}