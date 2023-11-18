<template>
  <main class="container pt-4">
    <div class="navbar">
      <router-link class="nav-link" :to="{ name: 'MainPage' }">
        <i class="fas fa-home"></i> Main Page
      </router-link>
      <router-link class="nav-link" :to="{ name: 'NewArticle' }">
        New Article
      </router-link>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search articles..."
          @keyup.enter="performSearch"
        />
      </div>
      <router-link class="nav-link" :to="{ name: 'ProfilePage' }">
        <i class="fas fa-user-circle"></i> Profile Page
        <img
          class="profile-preview"
          src="https://via.placeholder.com/30"
          alt="Profile Preview"
      /></router-link>
    </div>
    <RouterView class="flex-shrink-0" />
  </main>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { RouterView } from 'vue-router'

export default defineComponent({
  components: { RouterView },
  data() {
    return {
      searchQuery: '',
    }
  },
  methods: {
    performSearch() {
      console.log('Performing search with query:', this.searchQuery)
      fetch('http://localhost:8000/api/search/', {
        method: 'POST',
        body: JSON.stringify({ search_string: this.searchQuery }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          if (data.id !== undefined){
            this.$router.push(`/article/${data.id}`)
            this.searchQuery = ''
          }
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
  },
})
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  color: #fff;
  padding: 10px;
}

.nav-link {
  text-decoration: none;
  color: #fff;
  margin: 0 10px;
  display: flex;
  align-items: center;
}

.nav-link i {
  margin-right: 5px;
}

.profile-preview {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-left: 5px;
}
</style>
