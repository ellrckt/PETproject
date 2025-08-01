import axios from "axios";

class RequestService {
   #baseUrl = 'http://localhost:8000';
   #requestHeader = axios.create({
      baseURL: this.#baseUrl,
      withCredentials: true,
   });

   constructor() {
      if (RequestService.instance) {
         return RequestService.instance;
      };
      RequestService.instance = this;
   }

   async request(method, url, data=null) {
      try {
         const res = await this.#requestHeader({
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

   get = async (url) => await this.request('get', url);

   post = async (url, data) => await this.request('post', url, data);

   put = async (url, data) => await this.request('put', url, data);

   delete = async (url) => await this.request('delete', url);

   patch = async (url, data) => await this.request('patch', url, data);
}


const reqService = new RequestService();

export default reqService;