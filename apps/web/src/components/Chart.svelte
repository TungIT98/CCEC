<script lang="ts">
  import * as echarts from 'echarts';
  import { onMount } from 'svelte';
  import { fetchClimateData } from '../lib/api';

  interface Props {
    type: 'temperature-rainfall' | 'co2-humidity';
  }

  const { type }: Props = $props();

  let chartEl: HTMLDivElement;
  let chart: echarts.ECharts;
  let loading = $state(true);
  let error = $state('');

  onMount(() => {
    chart = echarts.init(chartEl);
    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(chartEl);

    loadData();

    return () => {
      ro.disconnect();
      chart.dispose();
    };
  });

  async function loadData() {
    try {
      loading = true;
      const data = await fetchClimateData(21.0285, 105.8542, 30);
      if (type === 'temperature-rainfall') {
        renderTempRainChart(data);
      } else {
        renderCO2HumidityChart(data);
      }
    } catch (e: any) {
      error = 'Không tải được dữ liệu. Kiểm tra kết nối API.';
      console.warn(e);
    } finally {
      loading = false;
    }
  }

  function renderTempRainChart(data: any[]) {
    const timestamps = data.map(d => d.timestamp?.split('T')[0] || '').reverse();
    const temps = data.map(d => d.temperature).reverse();
    const rains = data.map(d => d.rainfall).reverse();

    chart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
      legend: { data: ['Nhiệt độ (°C)', 'Lượng mưa (mm)'], top: 0 },
      grid: { left: 40, right: 20, bottom: 30, top: 40 },
      xAxis: {
        type: 'category',
        data: timestamps,
        axisLabel: { fontSize: 10, color: '#64748b' },
      },
      yAxis: [
        { type: 'value', name: '°C', axisLabel: { fontSize: 10 }, splitLine: { lineStyle: { dashed: true } } },
        { type: 'value', name: 'mm', axisLabel: { fontSize: 10 }, splitLine: { show: false } },
      ],
      series: [
        {
          name: 'Nhiệt độ (°C)',
          type: 'line',
          yAxisIndex: 0,
          data: temps,
          smooth: true,
          lineStyle: { color: '#ef4444', width: 2 },
          itemStyle: { color: '#ef4444' },
          areaStyle: { color: 'rgba(239,68,68,0.1)' },
        },
        {
          name: 'Lượng mưa (mm)',
          type: 'bar',
          yAxisIndex: 1,
          data: rains,
          itemStyle: { color: 'rgba(59,130,246,0.7)' },
        },
      ],
    });
  }

  function renderCO2HumidityChart(data: any[]) {
    const timestamps = data.map(d => d.timestamp?.split('T')[0] || '').reverse();
    const co2 = data.map(d => d.co2_level).reverse();
    const humidity = data.map(d => d.humidity).reverse();

    chart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
      legend: { data: ['CO₂ (ppm)', 'Độ ẩm (%)'], top: 0 },
      grid: { left: 40, right: 20, bottom: 30, top: 40 },
      xAxis: {
        type: 'category',
        data: timestamps,
        axisLabel: { fontSize: 10, color: '#64748b' },
      },
      yAxis: [
        { type: 'value', name: 'ppm', axisLabel: { fontSize: 10 }, splitLine: { lineStyle: { dashed: true } } },
        { type: 'value', name: '%', min: 0, max: 100, axisLabel: { fontSize: 10 }, splitLine: { show: false } },
      ],
      series: [
        {
          name: 'CO₂ (ppm)',
          type: 'line',
          yAxisIndex: 0,
          data: co2,
          smooth: true,
          lineStyle: { color: '#f59e0b', width: 2 },
          itemStyle: { color: '#f59e0b' },
        },
        {
          name: 'Độ ẩm (%)',
          type: 'line',
          yAxisIndex: 1,
          data: humidity,
          smooth: true,
          lineStyle: { color: '#8b5cf6', width: 2 },
          itemStyle: { color: '#8b5cf6' },
          areaStyle: { color: 'rgba(139,92,246,0.1)' },
        },
      ],
    });
  }
</script>

<div bind:this={chartEl} class="w-full h-64"></div>
{#if loading}
  <div class="absolute inset-0 flex items-center justify-center bg-white/60">
    <span class="text-slate-400 text-sm">Đang tải biểu đồ...</span>
  </div>
{/if}
{#if error}
  <div class="mt-2 text-xs text-red-500">{error}</div>
{/if}