import { Navigate, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import UploadPage from "./pages/UploadPage";
import ResultPage from "./pages/ResultPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/upload" element={<UploadPage />} />
      <Route path="/result" element={<ResultPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
