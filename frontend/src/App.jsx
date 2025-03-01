import React from 'react';
import { DataProvider } from './DataContext';
import { Route, Routes } from "react-router-dom";
import Navbar from './components/NavBar';
import { Statistics } from "./components/pages";
import usePageLoader from './hooks/usePageLoader'; 

function App() {
    const loading = usePageLoader();

    return (
        <DataProvider>
            {loading && <Loader />}
            <Navbar />
            <Routes>
                <Route path="/" element={<Statistics />} />
            </Routes>
        </DataProvider>
    );
}

export default App;
