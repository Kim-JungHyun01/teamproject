package edu.team3.bootai.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration //환경설정용이라는 의미
public class WebClientConfig {
//    WebCilent를 구성하고 Bean으로 정의하여 애플리케이션에서 사용할 수 있도록 함
//    https://m.blog.naver.com/seek316/223337685249

    @Bean
    WebClient webClient(){
        return WebClient.builder().exchangeStrategies(ExchangeStrategies.builder()
                    .codecs(configurer -> configurer.defaultCodecs().maxInMemorySize(-1))
                    .build()).baseUrl("http://localhost:8001/") //파이썬 ai 서버주소
//                업로드한 파일을 ai 서버에 전송하기 위해서 버퍼의 크기를 제한을 제한없이(byteCount : -1) 진행
                .build();
    }//end webcilent


}//end class
