package prete_service.DTO;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
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
