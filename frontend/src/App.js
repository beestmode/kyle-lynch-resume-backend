import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ParchmentResume from "./components/ParchmentResume";
import { Toaster } from "./components/ui/toaster";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<ParchmentResume />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;