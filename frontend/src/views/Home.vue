<template>
  <div>
    <v-progress-linear color="primary" :active="isLoading" indeterminate absolute top></v-progress-linear>
    <h1 class="mb-8">Web tool for visualization of the IGS ROTI Maps product</h1>
    <v-alert
      text
      class="text-left"
      border="left"
      type="info">
      <strong>See for IGS ROTI Maps product:</strong><br>
      I. Cherniak, A. Krankowski, I. Zakharenkova.
      ROTI Maps: a new IGS ionospheric product characterizing the ionospheric irregularities occurrence.
      GPS Solutions 22, 69 (2018).
      <a href="https://doi.org/10.1007/s10291-018-0730-1" target="_blank">https://doi.org/10.1007/s10291-018-0730-1</a>
    </v-alert>
    <v-file-input
      label="File input"
      id="fileInput"
      prepend-icon=""
      @change="uploadFile"
      :disabled="isLoading"
      :error-messages="errorMessage"
      :success-messages="successMessage"
      outlined
      dense>
    </v-file-input>
    <a :class="{ 'd-none': pngData == '' }" :href="pngData" download="ROTI.png">Click to download image</a>
    <v-img :src="pngData"></v-img>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data: () => ({
    isLoading: false,
    errorMessage: '',
    successMessage: '',
    pngData: ''
  }),
  methods: {
    async uploadFile(file) {
      this.errorMessage = '';
      this.successMessage = '';
      this.pngData = '';
      if (file) {
        this.isLoading = true;
        const body = new FormData();
        body.append('file', file);
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        await axios.post('/api/plot-map', body, config)
        .then((response) => {
          this.pngData = response.data.png_data;
          this.successMessage = 'Done';
        })
        .catch((error) => {
          this.isError = true;
          const status = error.response.status;
          if (status == 400) {
            this.errorMessage = 'Unsupported file type';
          }
        })
        .then(() => {
          this.isLoading = false;
        });
      }
    }
  }
};
</script>
