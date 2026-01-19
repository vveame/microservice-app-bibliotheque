package prete_service.DTO;

import lombok.*;
import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class RequestPreteDTO {
    private String titre;
    private String description;
    private Date datePret;
    private Date dateFinPret;
    private Boolean livreRetourne;
    private Boolean demande;
    private String userId;
    private Integer idLivre;
}