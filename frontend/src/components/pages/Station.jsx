import React, { useEffect, useState } from 'react';
import './station.css';

function Progress() {
  const [aboveWater, setAboveWater] = useState(0); 
  const [underWater, setUnderWater] = useState(0); 

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/data_ground');
        const data = await response.json();
        console.log(data.data[data.data.length - 1])
        if (data && data.data && data.data[data.data.length - 1]) {
          const { above, under } = data.data[data.data.length - 1];
          setAboveWater(above)
          setUnderWater(under)
        }
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }

      console.log(aboveWater, underWater)

    };

    fetchData();

    const intervalId = setInterval(fetchData, 1000); 

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className='stationContainer'>
      <div className='camera_stream'>
        <img src="http://192.168.137.11:81/stream" alt="Camera is not connected" className='camera' />
        
        {/* Блок для воды */}
        {
        }
      </div>
      <div className='ground_station'>
        <img src="../../../public/ground.png" alt="Ground Station" className='ground_img' />
        <div className='waterAbove' style={{ height: `${aboveWater*1.5}px` }}></div>
        <div className='waterUnder' style={{ height: `${underWater*1.5}px` }}></div>
      </div>
    </div>
  );
}

export default Progress;
