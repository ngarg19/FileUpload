package springProject.FileUpload;

import java.io.ByteArrayInputStream;
import java.io.InputStream;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
// import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
// import org.springframework.web.multipart.MultipartFile;
// import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import com.google.cloud.storage.Blob;
import com.google.cloud.storage.BlobId;
import com.google.cloud.storage.Storage;

import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;

@RestController
public class FileDownloadController {

    @Autowired
    private FileMetadataRepository fileMetadataRepository;
    @Value("${gcp.storage.bucketName}")
    private String bucketName;
    private Storage storage;

    @GetMapping("/download/{shortLink}")
    public ResponseEntity<Resource> downloadFile(@PathVariable String shortLink) {
        FileMetaData fileMetadata = fileMetadataRepository.findByShortLink(shortLink);
        if (fileMetadata != null) {
            Resource fileResource = loadFileResource(fileMetadata.getOriginalFilename());
            if (fileResource != null) {
                return ResponseEntity.ok()
                        .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"" + fileMetadata.getOriginalFilename() + "\"")
                        .body(fileResource);
            }
        }
        return ResponseEntity.notFound().build();
    }

    private Resource loadFileResource(String fileName) {
        // Load the file from the storage system
        // Implement your logic to retrieve the file resource based on the file name
        // Return the file resource as a Resource object (e.g., InputStreamResource, UrlResource, etc.)
        // This will depend on how you have stored the files and the storage system you are using

        // Example implementation for Google Cloud Storage using GCP Storage API
        Blob blob = storage.get(BlobId.of(bucketName, fileName));
        if (blob != null && blob.exists()) {
            InputStream inputStream = new ByteArrayInputStream(blob.getContent());
            return new InputStreamResource(inputStream);
        }
        return null;
    }
}
