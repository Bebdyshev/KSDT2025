import React, { useContext, useMemo } from 'react';
import BuoyChart from './BuoyChart';
import BuoyMap from './Map';
import { DataContext } from '../../DataContext';
import './Statistics.css'; 

function Statistics() {
  const data = useContext(DataContext);
  
  const balloonHeight = useMemo(() => {
    if (data && data.length > 0) {
      const lastEntry = data[data.length - 1];
      // Нормализуем высоту от 0 до 100%
      return (lastEntry.height - 100) / (900 - 100) * 100;
    }
    return 0;
  }, [data]);

  return (
    <div className="statistics-container">
      <div className="map-container">
        <BuoyMap />
      </div>
      <div className="charts-container">
        <BuoyChart label="CH4" dataY="density" rgb="rgba(75, 192, 192, 1)" />
        <BuoyChart label="Temperature" dataY="temp" rgb="rgba(255, 99, 132, 1)" />
        <BuoyChart label="Height" dataY="height" rgb="rgba(54, 162, 235, 1)" />
        <BuoyChart label="CO2" dataY="ph" rgb="rgba(153, 102, 255, 1)" />
        <BuoyChart label="Pressure" dataY="pressure" rgb="rgba(255, 206, 86, 1)" />
        <BuoyChart label="Velocity" dataY="velocity" rgb="rgb(40, 167, 69)" />
      </div>
      <div className="balloon-container">
        <svg 
          viewBox="0 0 60 100" 
          className="balloon_svg"
          style={{ 
            bottom: `${Math.min(Math.max(balloonHeight, 0), 80)}%`,  
          }}
        >
          {/* Корзина */}
          <rect x="25" y="80" width="10" height="10" fill="#8B4513" />
          
          {/* Веревки */}
          <line x1="27" y1="50" x2="25" y2="80" stroke="#8B4513" strokeWidth="1" />
          <line x1="33" y1="50" x2="35" y2="80" stroke="#8B4513" strokeWidth="1" />
          
          {/* Шар */}
          <path
            d="M 30 10 
               C 15 10, 15 50, 30 50 
               C 45 50, 45 10, 30 10"
            fill="#FF6B6B"
            stroke="#FF4040"
            strokeWidth="1.5"
          />
          
          {/* Полоски на шаре */}
          <path
            d="M 30 10 
               C 22 10, 22 50, 30 50"
            fill="none"
            stroke="#FF4040"
            strokeWidth="0.8"
          />
          <path
            d="M 30 10 
               C 38 10, 38 50, 30 50"
            fill="none"
            stroke="#FF4040"
            strokeWidth="0.8"
          />
          
          {/* Верхушка шара */}
          <circle cx="30" cy="10" r="3" fill="#FF4040" />
        </svg>
      </div>
      <img src="/images/rocket.png" alt="Rocket" className='rocket_img' />
    </div>
  );
}

export default Statistics;
