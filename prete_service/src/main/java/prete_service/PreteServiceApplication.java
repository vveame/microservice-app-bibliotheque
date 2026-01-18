package prete_service;

import prete_service.configuration.RsaKeys;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableFeignClients
@EnableCaching
@EnableConfigurationProperties({RsaKeys.class})
@EnableDiscoveryClient

public class PreteServiceApplication {

    public static void main(String[] args) {
        SpringApplication.run(PreteServiceApplication.class, args);
    }

}
