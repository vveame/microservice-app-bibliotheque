package prete_service.repository;

import prete_service.entity.Prete;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Date;
import java.util.List;

public interface PreteRepository extends JpaRepository<Prete, Integer> {
    List<Prete> findByUserIdAndLivreRetourneFalse(String userId);

    // For anciennePrete: Loans that have been returned
    List<Prete> findByLivreRetourneTrue();

    // For preteActif: Active loans not yet returned and not expired
    @Query("SELECT p FROM Prete p WHERE p.livreRetourne = false " +
            "AND p.dateFinPret > :currentDate " +
            "AND (p.demande IS NULL OR p.demande = false)")
    List<Prete> findActivePretes(@Param("currentDate") Date currentDate);

    // For retardPrete: Overdue loans
    @Query("SELECT p FROM Prete p WHERE p.livreRetourne = false " +
            "AND p.dateFinPret < :currentDate " +
            "AND (p.demande IS NULL OR p.demande = false)")
    List<Prete> findOverduePretes(@Param("currentDate") Date currentDate);

    // For demandePrete: Get all loan requests
    List<Prete> findByDemandeTrue();

    // For getPretesOnly: Get all ACTUAL loans (not requests, not returned)
    @Query("SELECT p FROM Prete p WHERE p.demande = false")
    List<Prete> findAllActiveActualPretes();

    // For the lecteur's loan history
    @Query("SELECT p FROM Prete p WHERE p.userId = :userId AND p.demande = false ORDER BY p.datePret DESC")
    List<Prete> findUserLoanHistory(@Param("userId") String userId);

    // Get user's loan requests (demandes)
    @Query("SELECT p FROM Prete p WHERE p.userId = :userId AND p.demande = true ORDER BY p.datePret DESC")
    List<Prete> findUserDemandes(@Param("userId") String userId);
}
