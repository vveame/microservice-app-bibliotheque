package prete_service.service;

import jakarta.transaction.Transactional;
import prete_service.DTO.Lecteur;
import prete_service.DTO.Livre;
import prete_service.DTO.RequestPreteDTO;
import prete_service.DTO.ResponsePreteDTO;
import prete_service.FeignClient.LecteurClient;
import prete_service.FeignClient.LivreClient;
import prete_service.entity.Prete;
import prete_service.exception.ActiveLoanException;
import prete_service.exception.ExternalServiceException;
import prete_service.exception.InvalidOperationException;
import prete_service.exception.ResourceNotFoundException;
import prete_service.mappers.PreteMapper;
import prete_service.repository.PreteRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
public class PreteServiceImpl implements PreteService {
    private final PreteRepository preteRepository;
    private final PreteMapper preteMapper;
    private final LecteurClient lecteurClient;
    private final LivreClient livreClient;

    public PreteServiceImpl(PreteRepository preteRepository, PreteMapper preteMapper, LecteurClient lecteurClient, LivreClient livreClient) {
        this.preteRepository = preteRepository;
        this.preteMapper = preteMapper;
        this.lecteurClient = lecteurClient;
        this.livreClient = livreClient;
    }

    @Override
    public ResponsePreteDTO addPrete(RequestPreteDTO requestPreteDTO) {

        try {
            Lecteur lecteur = lecteurClient.getLecteurById(requestPreteDTO.getIdLecteur());
            if (lecteur == null) {
                throw new ResourceNotFoundException("Lecteur Introuvable !");
            }
        } catch (Exception e) {
            throw new ExternalServiceException("Erreur lors de la récupération du lecteur avec l'ID: " + requestPreteDTO.getIdLecteur(), e);
        }

        try {
            Livre livre = livreClient.getLivreById(requestPreteDTO.getIdLivre());
            if (livre == null) {
                throw new ResourceNotFoundException("Livre Introuvable !");
            }
        } catch (Exception e) {
            throw new ExternalServiceException("Erreur lors de la récupération du livre avec l'ID: " + requestPreteDTO.getIdLivre(), e);
        }

        //Check if user already has an active loan (livreRetourne = false)
        List<Prete> activePretes = preteRepository.findByIdLecteurAndLivreRetourneFalse(requestPreteDTO.getIdLecteur());

        // Only check for ACTUAL loans (demande = false), not loan requests
        // If you want to also prevent loan requests when user has active loan, remove the demande check
        boolean hasActiveLoan = activePretes.stream()
                .anyMatch(prete -> prete.getDemande() == null || !prete.getDemande());

        if (hasActiveLoan) {
            throw new ActiveLoanException(
                    "Le lecteur avec ID " + requestPreteDTO.getIdLecteur() +
                            " a déjà un prêt actif. Veuillez retourner le livre avant d'en emprunter un autre."
            );
        }

        Prete prete = preteMapper.DTO_to_Prete(requestPreteDTO);
        if (prete.getDemande() == null) {
            prete.setDemande(false);
        }
        if (prete.getLivreRetourne() == null) {
            prete.setLivreRetourne(false);
        }

        Prete savedPrete = preteRepository.save(prete);
        savedPrete.setLecteur(lecteurClient.getLecteurById(savedPrete.getIdLecteur()));
        savedPrete.setLivre(livreClient.getLivreById(savedPrete.getIdLivre()));
        return preteMapper.Prete_To_DTO(savedPrete);
    }

    @Override
    public List<ResponsePreteDTO> getAllPretes() {
        List<Prete> pretes = preteRepository.findAll();
        List<ResponsePreteDTO> result = new ArrayList<>();

        for (Prete p : pretes) {

            Lecteur lecteur = lecteurClient.getLecteurById(p.getIdLecteur());
            p.setLecteur(lecteur);
            Livre livre = livreClient.getLivreById(p.getIdLivre());
            p.setLivre(livre);
            ResponsePreteDTO dto = preteMapper.Prete_To_DTO(p);
            result.add(dto);
        }
        return result;
    }

    @Override
    public ResponsePreteDTO getPreteById(Integer id) {

        Prete prete = preteRepository.findById(id).orElse(null);
        if (prete == null) return null;

        Lecteur lecteur = lecteurClient.getLecteurById(prete.getIdLecteur());
        Livre livre = livreClient.getLivreById(prete.getIdLivre());

        prete.setLecteur(lecteur);
        prete.setLivre(livre);

        return preteMapper.Prete_To_DTO(prete);
    }

    @Override
    public void deletePrete(Integer id) {
        preteRepository.deleteById(id);
    }

    @Override
    public ResponsePreteDTO updatePrete(Integer idPrete, RequestPreteDTO requestPreteDTO) {

        Prete prete = preteRepository.findById(idPrete).orElse(null);
        Prete nv_prete = preteMapper.DTO_to_Prete(requestPreteDTO);

        if (nv_prete.getTitre() != null) {prete.setTitre(nv_prete.getTitre());}
        if (nv_prete.getDescription() != null) {prete.setDescription(nv_prete.getDescription());}
        if (nv_prete.getDatePret() != null) {prete.setDatePret(nv_prete.getDatePret());}
        if (nv_prete.getDateFinPret() != null) {prete.setDateFinPret(nv_prete.getDateFinPret());}
        if (nv_prete.getLivreRetourne() != null) {prete.setLivreRetourne(nv_prete.getLivreRetourne());}
        if (nv_prete.getDemande() != null) {prete.setDemande(nv_prete.getDemande());}
        if (nv_prete.getIdLecteur() != null) {prete.setIdLecteur(nv_prete.getIdLecteur());}
        if (nv_prete.getIdLivre() != null) {prete.setIdLivre(nv_prete.getIdLivre());}

        Prete saved_prete = preteRepository.save(prete);
        return preteMapper.Prete_To_DTO(saved_prete);
    }


    @Override
    @Transactional
    public ResponsePreteDTO retournerLivre(Integer idPret) {
        Prete prete = preteRepository.findById(idPret)
                .orElseThrow(() -> new ResourceNotFoundException("Prêt non trouvé avec ID: " + idPret));

        // Check if it's an actual loan (not a request)
        if (prete.getDemande() != null && prete.getDemande()) {
            throw new InvalidOperationException("Ceci est une demande de prêt, pas un prêt actif.");
        }

        // Check if book is already returned
        if (Boolean.TRUE.equals(prete.getLivreRetourne())) {
            throw new InvalidOperationException("Le livre a déjà été retourné.");
        }

        // Mark book as returned
        prete.setLivreRetourne(true);
        Prete savedPrete = preteRepository.save(prete);

        // Fetch user and book details for response
        savedPrete.setLecteur(lecteurClient.getLecteurById(savedPrete.getIdLecteur()));
        savedPrete.setLivre(livreClient.getLivreById(savedPrete.getIdLivre()));

        return preteMapper.Prete_To_DTO(savedPrete);
    }

    @Override
    @Transactional
    public ResponsePreteDTO extendPrete(Integer idPret, Date newDateFinPret) {
        Prete prete = preteRepository.findById(idPret)
                .orElseThrow(() -> new ResourceNotFoundException("Prêt non trouvé avec ID: " + idPret));

        // Check if it's an actual loan
        if (prete.getDemande() != null && prete.getDemande()) {
            throw new InvalidOperationException("Impossible de prolonger une demande de prêt.");
        }

        // Check if book is already returned
        if (Boolean.TRUE.equals(prete.getLivreRetourne())) {
            throw new InvalidOperationException("Impossible de prolonger un prêt déjà retourné.");
        }

        // Check if new date is after current end date
        if (newDateFinPret.before(prete.getDateFinPret())) {
            throw new InvalidOperationException("La nouvelle date de fin doit être après la date actuelle: " + prete.getDateFinPret());
        }

        // Update the end date
        prete.setDateFinPret(newDateFinPret);
        Prete savedPrete = preteRepository.save(prete);

        // Fetch user and book details
        savedPrete.setLecteur(lecteurClient.getLecteurById(savedPrete.getIdLecteur()));
        savedPrete.setLivre(livreClient.getLivreById(savedPrete.getIdLivre()));

        return preteMapper.Prete_To_DTO(savedPrete);
    }

    @Override
    public List<ResponsePreteDTO> anciennePrete() {
        List<Prete> pretes = preteRepository.findByLivreRetourneTrue();
        return convertPretesToDTOList(pretes);
    }

    @Override
    public List<ResponsePreteDTO> preteActif() {
        Date currentDate = new Date(); // Current system date/time
        List<Prete> pretes = preteRepository.findActivePretes(currentDate);
        return convertPretesToDTOList(pretes);
    }

    @Override
    public List<ResponsePreteDTO> retardPrete() {
        Date currentDate = new Date();
        List<Prete> pretes = preteRepository.findOverduePretes(currentDate);
        return convertPretesToDTOList(pretes);
    }

    @Override
    @Transactional
    public ResponsePreteDTO demandePrete(RequestPreteDTO requestPreteDTO) {
        // Validate user exists
        try {
            Lecteur lecteur = lecteurClient.getLecteurById(requestPreteDTO.getIdLecteur());
            if (lecteur == null) {
                throw new ResourceNotFoundException("Lecteur Introuvable !");
            }
        } catch (Exception e) {
            throw new ExternalServiceException("Lecteur avec l'ID: " + requestPreteDTO.getIdLecteur(), e);
        }

        // Validate book exists
        try {
            Livre livre = livreClient.getLivreById(requestPreteDTO.getIdLivre());
            if (livre == null) {
                throw new ResourceNotFoundException("Livre Introuvable !");
            }
        } catch (Exception e) {
            throw new ExternalServiceException("Erreur lors de la récupération du livre avec l'ID: " + requestPreteDTO.getIdLivre(), e);
        }

        // Create loan request
        Prete prete = preteMapper.DTO_to_Prete(requestPreteDTO);

        // Set specific values for loan request
        prete.setDemande(true);           // This is a request
        prete.setLivreRetourne(null);     // Not applicable for requests
        prete.setDatePret(new Date());    // Request date is now

        // If dateFinPret is not provided, set a default (e.g., 7 days from now)
        if (prete.getDateFinPret() == null) {
            long sevenDaysInMillis = 7L * 24 * 60 * 60 * 1000;
            prete.setDateFinPret(new Date(System.currentTimeMillis() + sevenDaysInMillis));
        }

        Prete savedPrete = preteRepository.save(prete);
        savedPrete.setLecteur(lecteurClient.getLecteurById(savedPrete.getIdLecteur()));
        savedPrete.setLivre(livreClient.getLivreById(savedPrete.getIdLivre()));

        return preteMapper.Prete_To_DTO(savedPrete);
    }

    @Override
    @Transactional
    public void rejeterPrete(Integer idPret) {
        Prete prete = preteRepository.findById(idPret)
                .orElseThrow(() -> new ResourceNotFoundException("Demande de prêt non trouvée avec ID: " + idPret));

        // Check if it's actually a request
        if (prete.getDemande() == null || !prete.getDemande()) {
            throw new InvalidOperationException("Ceci n'est pas une demande de prêt.");
        }

        preteRepository.delete(prete);
    }

    @Override
    @Transactional
    public ResponsePreteDTO accepterPrete(Integer idPret) {
        Prete prete = preteRepository.findById(idPret)
                .orElseThrow(() -> new ResourceNotFoundException("Demande de prêt non trouvée avec ID: " + idPret));

        // Check if it's actually a request
        if (prete.getDemande() == null || !prete.getDemande()) {
            throw new InvalidOperationException("Ceci n'est pas une demande de prêt.");
        }

        // Check if user already has an active loan
        List<Prete> activePretes = preteRepository.findByIdLecteurAndLivreRetourneFalse(prete.getIdLecteur());
        boolean hasActiveLoan = activePretes.stream()
                .anyMatch(p -> p.getDemande() == null || !p.getDemande());

        if (hasActiveLoan) {
            throw new ActiveLoanException(
                    "Le lecteur avec ID " + prete.getIdLecteur() +
                            " a déjà un prêt actif. Impossible d'accepter cette demande."
            );
        }

        // Convert request to actual loan
        prete.setDemande(false);
        prete.setLivreRetourne(false); // Now it's an active loan

        // Set actual loan dates if not already set
        if (prete.getDatePret() == null) {
            prete.setDatePret(new Date());
        }

        Prete savedPrete = preteRepository.save(prete);
        savedPrete.setLecteur(lecteurClient.getLecteurById(savedPrete.getIdLecteur()));
        savedPrete.setLivre(livreClient.getLivreById(savedPrete.getIdLivre()));

        return preteMapper.Prete_To_DTO(savedPrete);
    }

    @Override
    public List<ResponsePreteDTO> getAllDemandes() {
        // Get all loan requests (demande = true)
        List<Prete> demandePretes = preteRepository.findByDemandeTrue();

        return convertPretesToDTOList(demandePretes);
    }

    @Override
    public List<ResponsePreteDTO> getPretesOnly() {
        List<Prete> activePretes = preteRepository.findAllActiveActualPretes();

        return convertPretesToDTOList(activePretes);
    }

    // ============ HELPER METHOD ============

    private List<ResponsePreteDTO> convertPretesToDTOList(List<Prete> pretes) {
        List<ResponsePreteDTO> result = new ArrayList<>();

        for (Prete p : pretes) {
            Lecteur lecteur = lecteurClient.getLecteurById(p.getIdLecteur());
            Livre livre = livreClient.getLivreById(p.getIdLivre());

            p.setLecteur(lecteur);
            p.setLivre(livre);

            ResponsePreteDTO dto = preteMapper.Prete_To_DTO(p);
            result.add(dto);
        }

        return result;
    }
}