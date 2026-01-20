package prete_service.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.util.Date;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
public class Lecteur {
    @JsonProperty("userId")
    private String userId;

    private String nom;
    private String prenom;
    private String date_naissance;
    private String email;
    private String password;
    private String role;
    private Date created_at;
    private Date updated_at;
}
