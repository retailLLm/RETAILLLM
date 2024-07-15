import React from 'react';

import SearchBar from './SearchComponent';
import AnalysisSection from './AnalysisSection';
import "./AnalysisSection.css"
function App() {
  return (
    <div className="App">
    
    <header className="header">
      <h1>Sales Analysis Dashboard</h1>
    </header>
      <SearchBar />
      <div className="analysis-container">
        <AnalysisSection title="Over Time Sales" />
        <AnalysisSection title="Seasonal Trends" />
        <AnalysisSection title="Best Performance" />
        <AnalysisSection title="Worst Performance" />
        <AnalysisSection title="Average Daily Sales" />
        <AnalysisSection title="Sales Distribution" />
        <AnalysisSection title="Christmas Season Sales" />
      </div>
    </div>
  );
}

export default App;
