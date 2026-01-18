package prete_service.DTO;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Livre {
    private Integer idLivre;
    private String titre;
    private String auteur;
    private String genre;
    private String isbn;
    private Integer numChapters;
    private Integer numPages;
    private Integer numTotalLivres;
}
