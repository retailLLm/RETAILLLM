import React from 'react';

function AnalysisSection({ title }) {
  return (
    <div className="analysis-section">
      <h2>{title}</h2>
      <div className="chart">
        {/* Chart will be inserted here */}
      </div>
    </div>
  );
}

export default AnalysisSection;
