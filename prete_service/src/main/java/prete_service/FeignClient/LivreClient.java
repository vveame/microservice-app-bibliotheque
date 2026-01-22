package prete_service.FeignClient;

import io.github.resilience4j.bulkhead.annotation.Bulkhead;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import prete_service.DTO.Livre;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "LIVRE-SERVICE", url = "${livre.service.url}")
public interface LivreClient {
    @GetMapping("/v1/livres/{id}")
    @CircuitBreaker(name = "livreCB", fallbackMethod = "fallbackGetLivre")
    @Retry(name = "livreRetry",fallbackMethod = "fallbackGetLivre")
    @Bulkhead(name = "livreBull",fallbackMethod = "fallbackGetLivre")
    @Cacheable(value = "livre-cache", key = "#id", unless = "#result == null")
    Livre getLivreById(@PathVariable("id") Integer id);

    @PutMapping("/v1/livres/{id}/decrement")
    @CircuitBreaker(name = "livreCB", fallbackMethod = "fallbackGetLivre")
    @Retry(name = "livreRetry", fallbackMethod = "fallbackGetLivre")
    @Bulkhead(name = "livreBull", fallbackMethod = "fallbackGetLivre")
    Livre decrementLivreStock(@PathVariable("id") Integer id);

    @PutMapping("/v1/livres/{id}/increment")
    @CircuitBreaker(name = "livreCB", fallbackMethod = "fallbackGetLivre")
    @Retry(name = "livreRetry", fallbackMethod = "fallbackGetLivre")
    @Bulkhead(name = "livreBull", fallbackMethod = "fallbackGetLivre")
    Livre incrementLivreStock(@PathVariable("id") Integer id);

    default Livre fallbackGetLivre(Integer id, Throwable t) {
        Livre fallbackLivre = new Livre();
        fallbackLivre.setIdLivre(id);
        fallbackLivre.setTitre("Livre Indisponible");
        fallbackLivre.setAuteur("Auteur Inconnu");
        System.err.println("Fallback triggered for livre ID: " + id + " - Error: " + t.getMessage());
        return fallbackLivre;
    }
}