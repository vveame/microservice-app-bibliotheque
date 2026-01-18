package prete_service.service;

import prete_service.DTO.RequestPreteDTO;
import prete_service.DTO.ResponsePreteDTO;

import java.util.Date;
import java.util.List;

public interface PreteService {
    ResponsePreteDTO addPrete(RequestPreteDTO requestPreteDTO);
    List<ResponsePreteDTO> getAllPretes();
    ResponsePreteDTO getPreteById(Integer id);
    void deletePrete(Integer id);
    ResponsePreteDTO updatePrete(Integer id, RequestPreteDTO requestPreteDTO);

    ResponsePreteDTO retournerLivre(Integer idPret);  // Mark book as returned
    ResponsePreteDTO extendPrete(Integer idPret, Date newDateFinPret);  // Extend loan period
    List<ResponsePreteDTO> anciennePrete();  // List returned loans
    List<ResponsePreteDTO> preteActif();  // List active loans (not returned, not expired)
    List<ResponsePreteDTO> retardPrete();  // List overdue loans
    ResponsePreteDTO demandePrete(RequestPreteDTO requestPreteDTO);  // Create loan request
    void rejeterPrete(Integer idPret);  // Reject loan request
    ResponsePreteDTO accepterPrete(Integer idPret);  // Accept loan request
    List<ResponsePreteDTO> getAllDemandes(); // // List all loan requests

    // New method for ML recommendations
    List<ResponsePreteDTO> getPretesOnly();  // Get only active actual loans
    // History method
    List<ResponsePreteDTO> getUserLoanHistory(String idLecteur);
}
