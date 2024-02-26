import { createBrowserRouter } from "react-router-dom";

import * as Components from "./components";
import { Home } from "./pages/home";
import { ListBoletos } from "./pages/boletos/list";
import { UploadBoleto } from "./pages/boletos/upload";
import { Boletos } from "./pages/boletos";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Components.Layout />,
    errorElement: <Components.NoMatch />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "boletos",
        element: <Boletos />,
        children: [
          {
            path: "",
            element: <ListBoletos />,
          },
          {
            path: "upload",
            element: <UploadBoleto />,
          },
        ],
      },
    ],
  },
]);

export { router };
