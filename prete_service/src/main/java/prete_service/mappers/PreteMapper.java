package prete_service.mappers;

import prete_service.DTO.RequestPreteDTO;
import prete_service.DTO.ResponsePreteDTO;
import prete_service.entity.Prete;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Component;

@Component
public class PreteMapper {

    public Prete DTO_to_Prete(RequestPreteDTO requestPreteDTO) {
        Prete prete = new Prete();
        BeanUtils.copyProperties(requestPreteDTO, prete);
        return prete;
    }

    public ResponsePreteDTO Prete_To_DTO(Prete prete) {
        ResponsePreteDTO responsePreteDTO = new ResponsePreteDTO();
        BeanUtils.copyProperties(prete, responsePreteDTO);
        return responsePreteDTO;
    }
}