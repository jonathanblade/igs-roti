<template>
  <div>
    <v-progress-linear color="primary" :active="isLoading" indeterminate absolute top></v-progress-linear>
    <h1 class="mb-8">IGS ROTI Maps Database</h1>
    <v-date-picker
      v-model="date"
      first-day-of-week="1"
      :allowed-dates="getAllowedDates"
      @change="getMap"
      full-width>
    </v-date-picker>
    <a :class="{ 'd-none': pngData == '' }" :href="pngData" :download="getImageFilename()">Click to download image</a>
    <v-img :src="pngData"></v-img>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Database',
  data: () => ({
    isLoading: false,
    date: '',
    allowedDates: [],
    pngData: ''
  }),
  async mounted() {
    await this.getDates();
    this.date = this.allowedDates.slice(-1)[0];
    await this.getMap(this.date);
  },
  methods: {
    getImageFilename() {
      return `ROTI-${this.date}.png`
    },
    getAllowedDates(date) {
      for (var i = 0; i < this.allowedDates.length; i++) {
        if (this.allowedDates[i] == date) {
          return date;
        }
      }
    },
    async getDates() {
      this.isLoading = true;
      await axios.get('/api/dates')
      .then((response) => {
        const data = response.data;
        for (var i = 0; i < data.length; i++) {
          this.allowedDates.push(data[i]['date']);
        }
      })
      .then(() => {
        this.isLoading = false;
      });
    },
    async getMap(date) {
      this.isLoading = true;
      await axios.get('/api/map', {params: {date: date}})
      .then((response) => {
        this.pngData = response.data['png_data'];
      })
      .then(() => {
        this.isLoading = false;
      });
    }
  }
};
</script>
