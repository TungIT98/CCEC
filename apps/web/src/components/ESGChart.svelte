<script lang="ts">
  import * as echarts from 'echarts';
  import { onMount } from 'svelte';

  const API_BASE = import.meta.env.PUBLIC_API_URL ?? 'http://localhost:8000';

  let chartEl: HTMLDivElement;
  let chart: echarts.ECharts;
  let loading = $state(true);
  let error = $state('');
  let activeTab = $state<'score' | 'trend' | 'compare'>('score');

  // Demo ESG data
  const demoData = {
    companies: ['Vingroup', 'Viettel', 'FPT', 'PVN', 'VN Airlines', 'Samsung Vina'],
    scores: [78, 82, 85, 61, 55, 74],
    envScores: [72, 79, 83, 58, 52, 70],
    socScores: [81, 85, 88, 62, 57, 76],
    govScores: [82, 83, 84, 64, 57, 78],
    trend: [65, 68, 70, 73, 75, 78],
  };

  onMount(() => {
    chart = echarts.init(chartEl);
    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(chartEl);
    loadData();
    return () => { ro.disconnect(); chart.dispose(); };
  });

  async function loadData() {
    loading = true;
    try {
      const res = await fetch(`${API_BASE}/api/v1/esg/scores`, {
        headers: authHeaders(),
      });
      if (res.ok) {
        const data = await res.json();
        renderChart(data);
      } else {
        renderChart(demoData);
      }
    } catch {
      renderChart(demoData);
    } finally {
      loading = false;
    }
  }

  function authHeaders(): Record<string, string> {
    try {
      const raw = localStorage.getItem('ccec_tokens');
      if (raw) {
        const tokens = JSON.parse(raw);
        return { Authorization: `Bearer ${tokens.access_token}` };
      }
    } catch {}
    return {};
  }

  function renderChart(data: typeof demoData) {
    if (activeTab === 'score') {
      renderScoreChart(data);
    } else if (activeTab === 'trend') {
      renderTrendChart(data);
    } else {
      renderCompareChart(data);
    }
  }

  function renderScoreChart(data: typeof demoData) {
    const sorted = [...data.companies].map((name, i) => ({ name, score: data.scores[i] }))
      .sort((a, b) => b.score - a.score);

    chart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { left: 140, right: 40, bottom: 20, top: 20 },
      xAxis: { type: 'value', min: 0, max: 100, axisLabel: { fontSize: 10, color: '#64748b' } },
      yAxis: { type: 'category', data: sorted.map(s => s.name), axisLabel: { fontSize: 11, color: '#475569' } },
      series: [{
        type: 'bar',
        data: sorted.map(s => ({
          value: s.score,
          itemStyle: {
            color: s.score >= 80 ? '#14b8a6' : s.score >= 60 ? '#f59e0b' : '#ef4444',
          },
        })),
        barWidth: 20,
        label: { show: true, position: 'right', fontSize: 11, color: '#64748b', formatter: '{c}/100' },
      }],
    });
  }

  function renderTrendChart(data: typeof demoData) {
    const years = ['2020', '2021', '2022', '2023', '2024', '2025(P)'];
    const sectors = ['Năng lượng', 'Công nghệ', 'Tài chính', 'Sản xuất'];
    const sectorScores = [
      [55, 58, 62, 67, 71, 74],
      [68, 72, 76, 80, 83, 85],
      [70, 73, 75, 77, 79, 82],
      [60, 63, 66, 69, 72, 75],
    ];

    chart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: sectors, top: 0, textStyle: { fontSize: 11 } },
      grid: { left: 40, right: 20, bottom: 30, top: 40 },
      xAxis: { type: 'category', data: years, axisLabel: { fontSize: 10, color: '#64748b' } },
      yAxis: { type: 'value', min: 40, max: 100, axisLabel: { fontSize: 10 }, splitLine: { lineStyle: { dashed: true } } },
      series: sectors.map((name, i) => ({
        name, type: 'line', data: sectorScores[i], smooth: true,
        lineStyle: { width: 2 },
        itemStyle: { color: ['#14b8a6', '#3b82f6', '#8b5cf6', '#f59e0b'][i] },
        areaStyle: { color: `${['#14b8a6', '#3b82f6', '#8b5cf6', '#f59e0b'][i]}15` },
      })),
    });
  }

  function renderCompareChart(data: typeof demoData) {
    chart.setOption({
      tooltip: { trigger: 'axis', axisPointer: { type: 'none' } },
      legend: { data: ['Môi trường', 'Xã hội', 'Quản trị'], top: 0 },
      grid: { left: 40, right: 20, bottom: 30, top: 40 },
      xAxis: { type: 'category', data: data.companies, axisLabel: { fontSize: 10, rotate: 15, color: '#64748b' } },
      yAxis: { type: 'value', max: 100, axisLabel: { fontSize: 10 }, splitLine: { lineStyle: { dashed: true } } },
      series: [
        { name: 'Môi trường', type: 'bar', data: data.envScores, itemStyle: { color: '#14b8a6' } },
        { name: 'Xã hội', type: 'bar', data: data.socScores, itemStyle: { color: '#3b82f6' } },
        { name: 'Quản trị', type: 'bar', data: data.govScores, itemStyle: { color: '#8b5cf6' } },
      ],
    });
  }

  $effect(() => {
    if (chart) renderChart(demoData);
  });

  const totalScore = (demoData.scores.reduce((a, b) => a + b, 0) / demoData.scores.length).toFixed(0);
</script>

<div class="space-y-6">
  <!-- E/S/G breakdown scores -->
  <div class="grid grid-cols-3 gap-4">
    {#each [['E', 'Môi trường', '72', '#14b8a6'], ['S', 'Xã hội', '79', '#3b82f6'], ['G', 'Quản trị', '75', '#8b5cf6']] as [letter, label, score, color]}
      <div class="bg-[#1E293B] border border-[#334155] rounded-xl p-4 text-center">
        <div class="text-3xl font-bold" style="color:{color}">{score}</div>
        <div class="text-xs text-[#94A3B8] mt-1">{letter} — {label}</div>
        <div class="mt-2 h-1.5 bg-[#334155] rounded-full overflow-hidden">
          <div class="h-full rounded-full transition-all" style="width:{score}%;background:{color}"></div>
        </div>
      </div>
    {/each}
  </div>

  <!-- Tabs -->
  <div class="flex gap-2">
    {#each [['score', 'Điểm ESG'], ['trend', 'Xu hướng'], ['compare', 'So sánh E/S/G']] as [tab, label]}
      <button onclick={() => { activeTab = tab as any; renderChart(demoData); }}
        class="px-4 py-1.5 text-sm rounded-full font-medium transition-colors {activeTab === tab ? 'bg-amber-600 text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white border border-[#334155]'}">
        {label}
      </button>
    {/each}
  </div>

  <!-- Chart -->
  <div bind:this={chartEl} class="w-full h-64"></div>

  {#if loading}
    <div class="text-center py-6">
      <div class="w-6 h-6 border-2 border-amber-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
    </div>
  {/if}

  <p class="text-xs text-[#64748b] text-center">
    Nguồn: Sustainalytics, MSCI ESG Ratings, Bloomberg ESG. (P) = Prophet forecast.
  </p>
</div>