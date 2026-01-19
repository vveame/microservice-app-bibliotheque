package security_service.service;

import org.springframework.security.core.GrantedAuthority;

import java.util.List;

public class CustomUserDetails extends org.springframework.security.core.userdetails.User {
    private final String userId;

    public CustomUserDetails(String userId, String username, String password, List<GrantedAuthority> authorities) {
        super(username, password, authorities);
        this.userId = userId;
    }

    public String getUserId() {
        return userId;
    }
}

