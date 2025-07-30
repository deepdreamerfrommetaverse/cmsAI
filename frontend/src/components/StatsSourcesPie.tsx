import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import React from 'react';

interface SourcesProps {
  sources: { [key: string]: number };
}

const StatsSourcesPie: React.FC<SourcesProps> = ({ sources }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const data = {
      labels: Object.keys(sources),
      datasets: [{
        data: Object.values(sources),
        backgroundColor: ['#1DA1F2', '#E1306C', '#888']
      }]
    };
    // Create chart instance
    const chart = new Chart(canvasRef.current, {
      type: 'pie',
      data,
      options: { plugins: { legend: { position: 'bottom' } } }
    });
    return () => chart.destroy();
  }, [sources]);

  return <canvas ref={canvasRef} width={200} height={200}></canvas>;
};

export default StatsSourcesPie;
