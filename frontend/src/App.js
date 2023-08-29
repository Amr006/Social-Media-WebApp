import { Box } from "@mui/material";
import { Outlet } from "react-router-dom";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";

function App() {
  return (
    <Box component={"main"}>
      <Header />
      <Outlet />
      <Footer />
    </Box>
  );
}

export default App;
