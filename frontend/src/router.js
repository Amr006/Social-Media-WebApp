import {
  createBrowserRouter,
} from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <></>,
    children: [
      {
        path: process.env.REACT_APP_LOGIN_PAGE,
        element: <></>,
      },
      {
        path: process.env.REACT_APP_REGISTER_PAGE,
        element: <></>,
      },
      {
        path: process.env.REACT_APP_ABOUT_PAGE,
        element: <></>,
      },
    ],
  },
]);
