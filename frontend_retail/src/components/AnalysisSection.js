import React, { useState, useEffect } from 'react';

const fetchImage = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const blob = await response.blob();
    const imageUrl = URL.createObjectURL(blob);
    return imageUrl;
  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
  }
};

function AnalysisSection({ title }) {
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    const loadImage = async () => {
      const img = await fetchImage();
      setImageUrl(img);
    };

    loadImage();
  }, []);

  return (
    <div className="analysis-section">
      <h2>{title}</h2>
      <div className="chart">
        {/* Display the image if it is loaded */}
        {imageUrl ? (
          <img src={imageUrl} alt="Analysis Chart" />
        ) : (
          <p>Loading image...</p>
        )}
      </div>
    </div>
  );
}

export default AnalysisSection;