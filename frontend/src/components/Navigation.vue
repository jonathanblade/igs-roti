<template>
  <v-breadcrumbs class="justify-center" :items="items" divider="|"></v-breadcrumbs>
</template>

<script>
export default {
  name: 'Navigation',
  data: () => ({
    items: [
      {
        text: 'Home',
        disabled: false,
        href: '/',
      },
      {
        text: 'Database',
        disabled: false,
        href: '/db',
      }
    ]
  })
};
</script>
