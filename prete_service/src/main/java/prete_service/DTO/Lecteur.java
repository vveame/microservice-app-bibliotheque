package prete_service.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Lecteur {
    @JsonProperty("userId")
    private String userId;

    private String nom;
    private String prenom;
    private String date_naissance;
    private String email;
    private String password;
    private String role;
}
