package security_service.web;

import org.springframework.http.HttpStatus;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.server.ResponseStatusException;
import security_service.dto.*;
import security_service.service.CustomUserDetails;
import security_service.service.DetailsService;
import org.springframework.security.authentication.*;
import org.springframework.security.core.*;
import org.springframework.security.oauth2.jwt.*;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.stream.Collectors;

@RestController
public class AuthApi {

    private final AuthenticationManager authenticationManager;
    private final JwtEncoder jwtEncoder;
    private final JwtDecoder jwtDecoder;
    private final DetailsService detailsService;

    public AuthApi(AuthenticationManager authenticationManager,
                          JwtEncoder jwtEncoder,
                          JwtDecoder jwtDecoder,
                          DetailsService detailsService) {
        this.authenticationManager = authenticationManager;
        this.jwtEncoder = jwtEncoder;
        this.jwtDecoder = jwtDecoder;
        this.detailsService = detailsService;
    }

    @PostMapping("/login")
    public TokenResponse login(@RequestBody LoginRequest request) {

        Authentication authentication =
                authenticationManager.authenticate(
                        new UsernamePasswordAuthenticationToken(
                                request.email() + ":" + request.role(),
                                request.password()
                        )
                );

        Instant now = Instant.now();
        String scope = authentication.getAuthorities()
                .stream().map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(" "));

        // Extract the userId from principal
        CustomUserDetails userDetails = (CustomUserDetails) authentication.getPrincipal();
        String userId = userDetails.getUserId();

        JwtClaimsSet accessClaims = JwtClaimsSet.builder()
                .subject(authentication.getName()) // email:role
                .issuer("security-service")
                .issuedAt(now)
                .expiresAt(now.plus(10, ChronoUnit.MINUTES))
                .claim("scope", scope)
                .claim("userId", userId)
                .build();

        JwtClaimsSet refreshClaims = JwtClaimsSet.builder()
                .subject(authentication.getName())
                .issuer("security-service")
                .issuedAt(now)
                .expiresAt(now.plus(30, ChronoUnit.MINUTES))
                .build();

        return new TokenResponse(
                jwtEncoder.encode(JwtEncoderParameters.from(accessClaims)).getTokenValue(),
                jwtEncoder.encode(JwtEncoderParameters.from(refreshClaims)).getTokenValue()
        );
    }

    @PostMapping("/refresh")
    public TokenResponse refresh(@RequestParam String refresh_token) {
        try {
            // Decode refresh token
            Jwt decoded = jwtDecoder.decode(refresh_token);

            String subject = decoded.getSubject(); // expected format: "email:role"
            if (subject == null || !subject.contains(":")) {
                throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid token subject");
            }

            // Load user details using combined subject
            UserDetails user = detailsService.loadUserByUsername(subject);

            Instant now = Instant.now();

            // Collect authorities to scope string
            String scope = user.getAuthorities()
                    .stream().map(GrantedAuthority::getAuthority)
                    .collect(Collectors.joining(" "));

            String userId = "";
            if(user instanceof CustomUserDetails) {
                userId = ((CustomUserDetails) user).getUserId();
            }

            // Build new access token claims
            JwtClaimsSet accessClaims = JwtClaimsSet.builder()
                    .subject(subject)
                    .issuer("security-service")
                    .issuedAt(now)
                    .expiresAt(now.plus(10, ChronoUnit.MINUTES))
                    .claim("scope", scope)
                    .claim("userId", userId)
                    .build();

            // Build new refresh token claims (rotated refresh token)
            JwtClaimsSet newRefreshClaims = JwtClaimsSet.builder()
                    .subject(subject)
                    .issuer("security-service")
                    .issuedAt(now)
                    .expiresAt(now.plus(30, ChronoUnit.MINUTES))
                    .build();

            // Encode and return tokens
            return new TokenResponse(
                    jwtEncoder.encode(JwtEncoderParameters.from(accessClaims)).getTokenValue(),
                    jwtEncoder.encode(JwtEncoderParameters.from(newRefreshClaims)).getTokenValue()
            );

        } catch (JwtValidationException e) {
            if (e.getMessage().contains("expired")) {
                throw new ResponseStatusException(HttpStatus.UNAUTHORIZED,
                        "Refresh token has expired. Please login again.", e);
            } else {
                throw new ResponseStatusException(HttpStatus.UNAUTHORIZED,
                        "Invalid refresh token: " + e.getMessage(), e);
            }
        }
    }
}