package prete_service.entity;

import jakarta.persistence.*;
import lombok.*;
import prete_service.DTO.Lecteur;
import prete_service.DTO.Livre;

import java.util.Date;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Entity
public class Prete {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer idPret;

    private String titre;
    private String description;
    private Date datePret;
    private Date dateFinPret;
    private Boolean livreRetourne;
    private Boolean demande;
    private String userId;
    private Integer idLivre;

    @Transient //l'attribue n'est pas représenter dans la DB ----> n'est persistant.
    private Lecteur lecteur;
    @Transient
    private Livre livre;
}