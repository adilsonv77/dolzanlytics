<template>
    <div style="position: relative; height: 80vh; width: 65vw;">
        <canvas ref="chart"></canvas>
    </div>
</template>
  
<script>
import { Chart } from 'chart.js/auto';

Chart.defaults.color = 'hsla(0,0%,100%,.8)';
Chart.defaults.font.size = 14;

export default {
    props: [
        'info'
    ],
    mounted() {
        this.renderChart()
    },
    methods: {
        renderChart() {
            const ctx = this.$refs.chart.getContext('2d');

            new Chart(ctx, {
                type: this.info["type"],
                options: {
                    responsive: true, 
                    maintainAspectRatio: false
                },
                data: this.info["data"]
            });
        },
    },
};
</script>
  
<style scoped></style>
  