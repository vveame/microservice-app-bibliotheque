package security_service.FeignClient;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;

import java.util.Map;

@FeignClient(name = "BIBLIOTHECAIRE-SERVICE", url = "${bibliothecaire.service.url}")
public interface BibliothecaireClient {

    @GetMapping("/internal/email/{email}")
    Map<String, Object> getByEmail(
            @PathVariable String email,
            @RequestHeader("X-API-KEY") String apiKey
    );
}