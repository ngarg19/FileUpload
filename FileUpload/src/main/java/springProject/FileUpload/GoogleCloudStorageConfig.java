package springProject.FileUpload;
import java.io.IOException;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;
import org.springframework.core.io.Resource;

@Configuration
public class GoogleCloudStorageConfig {

    @Value("${spring.cloud.gcp.credentials.location}")
    private Resource credentialsLocation;

    @Bean
    public Storage storage() throws IOException {
        return StorageOptions.newBuilder()
                .setCredentials(GoogleCredentials.fromStream(credentialsLocation.getInputStream()))
                .build()
                .getService();
    }
}

