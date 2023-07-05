package springProject.FileUpload;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FileMetadataRepository extends JpaRepository<FileMetaData, Long> {
    FileMetaData findByShortLink(String shortLink);

}

