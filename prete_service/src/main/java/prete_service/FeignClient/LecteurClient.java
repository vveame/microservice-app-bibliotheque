package prete_service.FeignClient;

import io.github.resilience4j.bulkhead.annotation.Bulkhead;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import org.springframework.web.bind.annotation.RequestHeader;
import prete_service.DTO.Lecteur;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "LECTEUR-SERVICE", url = "${lecteur.service.url}")
public interface LecteurClient {
    @GetMapping("/internal/lecteurs/{id}")
    @CircuitBreaker(name = "lecteurCB", fallbackMethod = "fallbackGetLecteur")
    @Retry(name = "lecteurRetry",fallbackMethod = "fallbackGetLecteur")
    @Bulkhead(name = "lecteurBull",fallbackMethod = "fallbackGetLecteur")
    @Cacheable(value = "lecteur-cache", key = "#id", unless = "#result == null")
    Lecteur getLecteurById(
            @PathVariable("id") String id,
            @RequestHeader("X-API-KEY") String apiKey
    );

    // Fallback method
    default Lecteur fallbackGetLecteur(String id, String apiKey, Throwable t) {
        // Create a default/empty lecteur
        Lecteur fallbackLecteur = new Lecteur();
        fallbackLecteur.setUserId(id);
        fallbackLecteur.setNom("Service Temporairement Indisponible");
        fallbackLecteur.setEmail("default@example.com");
        // Log the error
        System.err.println("Fallback triggered for lecteur ID: " + id + " - Error: " + t.getMessage());
        return fallbackLecteur;
    }
}