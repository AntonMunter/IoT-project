import React, { useEffect, useState } from "react";
import api from "../middleware/api";
import { ResponsiveBullet } from '@nivo/bullet'
import "./home.scss"


const timeout = 1000 * 10

const Home = () => {
  const [moist, setMoist] = useState([])
  const [temp, setTemp] = useState([])


  useEffect(() => {
    async function fetch() {
      try {
        const response = await api(1)
        if (!response.ok) {
          throw Error(response.statusText);
        }
        
        const json = await response.json();
        setMoist(moist => [
          {
            "id": "Moisture",
            "ranges": [
              200,
              400,
              800,
              1200,
              2000
            ],
            "measures": [
              json[0]['moist_data']
            ],
            "markers": [
              1000
            ]
          }
        ])

        setTemp(temp => [
          {
            "id": "Temperature",
            "ranges": [
              0,
              10,
              20,
              30,
              40
            ],
            "measures": [
              json[0]['temp_data']
            ],
            "markers": [
              
            ]
          }
        ])

    
      } catch (error) {
        console.log(error);
      }
    }
    
    fetch()

    const interval = setInterval(() => {
      fetch()
    }, timeout);
    return () => clearInterval(interval);
  }, []);

  return(
    <div className='home-box'>
      <div className='home-moist-chart'>
        <ResponsiveBullet
        data={moist}
        layout="vertical"
        margin={{ top: 50, right: 90, bottom: 50, left: 90 }}
        spacing={46}
        titlePosition="before"
        titleAlign="start"
        titleOffsetX={-30}
        titleOffsetY={10}
        measureSize={0.2}
        rangeColors="purple_blue"
        measureColors="#ABE098"
        motionConfig="gentle"
    />
      </div>

      <div className='home-temp-chart'>
        <ResponsiveBullet
        data={temp}
        layout="vertical"
        margin={{ top: 50, right: 90, bottom: 50, left: 90 }}
        spacing={46}
        titlePosition="before"
        titleAlign="start"
        titleOffsetX={-30}
        titleOffsetY={10}
        measureSize={0.2}
        rangeColors="blue_green"
        measureColors="#7393B3"
        motionConfig="gentle"
    />
      </div>

      </div>
    );
    }


export default Home