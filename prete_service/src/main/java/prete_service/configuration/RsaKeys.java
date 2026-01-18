package prete_service.configuration;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.security.interfaces.RSAPublicKey;

@ConfigurationProperties("rsa")

public record RsaKeys(RSAPublicKey  publicKey) {
}
