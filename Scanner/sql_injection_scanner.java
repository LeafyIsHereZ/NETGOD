import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = {"org.Trojan.s"})
@MapperScan("org.kontol.memek.ngaceng")
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
