package security_service.dto;

public record TokenResponse(
        String access_token,
        String refresh_token
) {}
