import { createBrowserRouter } from "react-router-dom";

import Layout from "../components/Layout";
import HomePage from "../pages/HomePage";
import NotFound from "../components/NotFound";
import AboutPage from "../pages/AboutPage";
import SignupPage from "../pages/SignupPage";
import LoginPage from "../pages/LoginPage";
import ProfilePage from "../pages/ProfilePage";

export const router = createBrowserRouter(
   [
      {
         path: "/",
         element: <Layout />,
         errorElement: <NotFound />,
         children: [
            {
               path: "home",
               element: <HomePage />,
            },
            {
               path: "about",
               element: <AboutPage />,
            },
            {
               path: "signup",
               element: <SignupPage />,
            },
            {
               path: "login",
               element: <LoginPage />,
            },

            // User routes
            {
               path: "profile",
               element: <ProfilePage />,
            },
            // {
            //    path: "products/:productId",
            //    element: <ProductDetail />,
            // },

            {
               path: "*",
               element: <NotFound />,
            },
         ],
      },
   ],
   {
      basename: "/",
   }
);
