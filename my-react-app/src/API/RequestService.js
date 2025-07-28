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
         await this.#requestHeader({
            method: method,
            url: url,
            data: data
         });
      } catch (error) {
         console.log('error!!!');
      }
   }

   get(url) {
      this.request('get', url);
   }

   post(url, data) {
      this.request('post', url, data);
   }

   put(url, data) {
      return this.request('put', url, data);
   }

   delete(url) {
      return this.request('delete', url);
   }

   patch(url, data) {
      return this.request('patch', url, data);
   }

}


const reqService = new RequestService();

export default reqService;