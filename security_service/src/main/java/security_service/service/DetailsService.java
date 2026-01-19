package security_service.service;

import org.springframework.beans.factory.annotation.Value;
import security_service.FeignClient.*;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.*;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class DetailsService implements UserDetailsService {

    private final LecteurClient lecteurClient;
    private final AdminClient adminClient;
    private final BibliothecaireClient bibliothecaireClient;
    private final String internalApiKey;

    public DetailsService(LecteurClient lecteurClient,
                          AdminClient adminClient,
                          BibliothecaireClient bibliothecaireClient,
                          @Value("${internal.api.key}") String internalApiKey) {
        this.lecteurClient = lecteurClient;
        this.adminClient = adminClient;
        this.bibliothecaireClient = bibliothecaireClient;
        this.internalApiKey = internalApiKey;
    }

    @Override
    public UserDetails loadUserByUsername(String emailAndRole) {
        System.out.println("AUTH REQUEST: " + emailAndRole);

        String[] parts = emailAndRole.split(":");
        String email = parts[0];
        String role = parts[1].toUpperCase();

        Map<String, Object> user = switch (role) {
            case "LECTEUR" -> lecteurClient.getByEmail(email, internalApiKey);
            case "ADMIN" -> adminClient.getByEmail(email, internalApiKey);
            case "BIBLIOTHECAIRE" -> bibliothecaireClient.getByEmail(email, internalApiKey);
            default -> throw new UsernameNotFoundException("Invalid role");
        };

        String userId = (String) user.get("userId");

        return new CustomUserDetails(
                userId,
                (String) user.get("email"),
                (String) user.get("password"),
                List.of(new SimpleGrantedAuthority("ROLE_" + role))
        );
    }
}