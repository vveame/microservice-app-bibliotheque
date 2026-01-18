package security_service.dto;

public record LoginRequest(
        String email,
        String password,
        String role
) {}
