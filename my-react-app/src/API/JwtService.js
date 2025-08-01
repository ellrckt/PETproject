import axios from "axios";

class JwtService {
   #accessToken = '';
   #baseUrl = 'http://localhost:8000/';
   #authHeader;

   constructor() {
      if (JwtService.instance) {
         return JwtService.instance;
      };

      this.#authHeader = axios.create({
         baseURL: this.#baseUrl,
         withCredentials: true,
      });

      //добавление актуального токена в заголовки
      this.#authHeader.interceptors.request.use((config) => {
         if (this.#accessToken) {
            config.headers['Authorization'] = `Bearer ${this.#accessToken}`;
         }
         return config;
      });

      JwtService.instance = this;
   }

   getAccessToken() {
      return this.#accessToken;
   }

   setAccessToken(token) {
      this.#accessToken = token;
   }

   //перехват ошибки сервера в случае протухшего токена и его обновление
   setResponseInterceptors() {
      this.#authHeader.interceptors.response.use(
         res => {
            if (res.data && res.data.access_token) {
               this.setAccessToken(res.data.access_token);
            }
            return res;
         },
         async err => {
            if (axios.isAxiosError(err) && err.response.status === 401) {
               try {
                  const res = await this.get('/login/refresh');
                  this.setAccessToken(res.data.access_token);
                  //console.log('new token: ', res.data.access_token);
                  //вытаскиваем конфиг исходного запроса
                  const config = err.config;
                  //повторяем исходный запрос с новым токеном
                  return this.#authHeader.request(config);
               } catch (err) {
                  //alert('Failed to refresh token')
                  console.error('Failed to refresh token:', err);
               }
            }
            //можно сделать перенаправление на страницу логина
            console.log('other server error');
            return Promise.reject(err);
         }
      );
   }

   async authRequest(method, url, data=null) {
      try {
         const res = await this.#authHeader({
            method: method,
            url: url,
            data: data
         });
         return res;
      } catch (error) {
         if (error?.response?.data?.detail && typeof error.response.data.detail === 'string') {
            return error.response.data.detail;
         } else {
            return 'Произошла ошибка';
         }
      }
   }

   get = async (url) => await this.authRequest('get', url);

   post = async (url, data) => await this.authRequest('post', url, data);

   put = async (url, data) => await this.authRequest('put', url, data);

   delete = async (url) => await this.authRequest('delete', url);

   patch = async (url, data) => await this.authRequest('patch', url, data);

}


const jwtService = new JwtService();
jwtService.setResponseInterceptors();

export default jwtService;