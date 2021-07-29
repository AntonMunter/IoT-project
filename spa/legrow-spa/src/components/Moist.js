import React, { useEffect, useState } from "react";
import api from '../middleware/api'
import { ResponsiveLine } from '@nivo/line'
import "./moist.scss"
import moment from 'moment'

const theme = {
  "textColor": "#363030",
  "fontSize": 21,
  "axis": {
      "domain": {
          "line": {
              "stroke": "#777777",
              "strokeWidth": 0
          }
      },
      "ticks": {
          "line": {
              "stroke": "#777777",
              "strokeWidth": 4
          }
      }
  },
  "grid": {
      "line": {
          "stroke": "#dddddd",
          "strokeWidth": 2
      }
  }
}

const timeout = 1000 * 10

const Moist = () => {
  const [data, setData] = useState([{
    "id": "moist",
    "color": "hsl(232, 70%, 50%)",
    "data": []
}])

  useEffect(() => {
    async function fetch() {
      try {
        const response = await api(50)
        if (!response.ok) {
          throw Error(response.statusText);
        }
    
        const json = await response.json();
        let arr = []
        
        await json.map( el => (
          arr.unshift({'x': moment(new Date(el.date)).format('MMMM Do YYYY, h:mm:ss') ,'y': el.moist_data})
        ))

        setData(data => [{
          "id": "moist",
          "color": "hsl(232, 70%, 50%)",
          "data": arr
      }])
    
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
    <div className='moist-box'>
      <div className='moist-chart'>
        <ResponsiveLine
        data={data}
        theme={theme}
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: 'point' }}
        yScale={{ type: 'linear', min: '200', max: '2000', stacked: true, reverse: false }}
        curve="natural"
        axisTop={null}
        axisRight={null}
        axisBottom={null}
        axisLeft={null}
        areaBaselineValue={0}
        enableGridX={false}
        enableGridY={true}
        lineWidth={5}
        enablePoints={false}
        pointSize={5}
        pointColor={{ theme: 'background' }}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabelYOffset={-24}
        enableArea={true}
        areaOpacity={0.7}
        useMesh={true}
        legends={[]}
        colors={{ scheme: 'accent' }}
    />
      </div>
      </div>
    );
  }

export default Moist