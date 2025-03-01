  return (
    <div className='stationContainer'>
      <div className='camera_stream'>
        <img src="http://192.168.137.11:81/stream" alt="Camera is not connected" className='camera' />
      </div>
      <div className='ground_station'>
        <img src="/images/ground.png" alt="Ground Station" className='ground_img' />
        <div className='waterAbove' style={{ height: `${aboveWater*1.5}px` }}></div>
        <div className='waterUnder' style={{ height: `${underWater*1.5}px` }}></div>
      </div>
    </div>
  ); 