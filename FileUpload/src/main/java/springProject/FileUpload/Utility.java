package springProject.FileUpload;

import java.util.Random;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.*;

@RestController
public class Utility {

    private static final String CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    // private static final int LINK_LENGTH = 11;

    @GetMapping("generateShortLink")
    public static String generateShortLink() {
        StringBuilder sb = new StringBuilder();
        Random random = new Random();
        int max = 15;
        int min = 8;
        int LINK_LENGTH = (int)Math.floor(Math.random() * (max - min + 1) + min);
        sb.append("https://example.com/");
        for (int i = 0; i < LINK_LENGTH; i++) {
            int index = random.nextInt(CHARACTERS.length());
            sb.append(CHARACTERS.charAt(index));
        }
        return sb.toString();
    }
}
