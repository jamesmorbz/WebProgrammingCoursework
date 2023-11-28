<template>
  <main class="container pt-4" id="main-component">
    <div class="navbar">
      <router-link class="nav-link" :to="{ name: 'MainPage' }">
        <i class="fas fa-home"></i> Main Page
      </router-link>
      <router-link class="nav-link" :to="{ name: 'NewArticle' }">
        New Article
      </router-link>
      <div class="search-bar">
        <input v-model="searchQuery" type="text" placeholder="Search articles..." @keyup.enter="performSearch" />
      </div>
      <router-link class="nav-link" :to="{ name: 'ProfilePage' }">
        <i class="fas fa-user-circle"></i> Profile Page
        <!-- need ajax request to get user image -->
        <img class="profile-preview" :src="userAvatar" alt="Profile Preview" />
      </router-link>
      <a class="nav-link" href="http://localhost:8000/logout">Logout</a>
    </div>
    <RouterView class="flex-shrink-0" />
  </main>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { RouterView } from 'vue-router'
import testImage from './assets/test-avatar.jpg'

export default defineComponent({
  components: { RouterView },
  data() {
    return {
      searchQuery: '',
      userAvatar: '',
    }
  },
  created() {
    this.getUserAvatar()
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
          if (data.id !== undefined) {
            this.$router.push(`/article/${data.id}`)
            this.searchQuery = ''
          }
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    async getUserAvatar() {
      try {
        // const response = await fetch('getuseravatarurl', {
        //   method: 'GET',
        // });
        // if (response.ok) {
        //   const data = await response.json();
        //   this.userAvatar = data
        // }
        //temp
        this.userAvatar = testImage
      } catch (error) {
        console.log('Error fetching user avatar', error);
      }
    },
  },
})
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgb(22, 38, 54);
  color: #fff;
  padding: 10px;
}

.nav-link {
  text-decoration: none;
  color: #fff;
  margin: 0 10px;
  display: flex;
  align-items: center;
  position: relative; /* Added position relative to make positioning the underline easier */
}

.nav-link i {
  margin-right: 5px;
}

.nav-link::after {
  content: ''; /* Create an empty pseudo-element */
  display: block; /* Make it a block element */
  height: 2px; /* Set the height of the underline */
  width: 0; /* Initially set the width to 0, it will expand on hover */
  background-color: rgb(216, 231, 247); /* Set the color of the underline */
  position: absolute; /* Position it absolutely relative to the parent .nav-link */
  bottom: -2px; /* Position it just below the text */
  transition: width 0.3s ease; /* Add a transition effect for a smoother appearance */
}

.nav-link:hover::after {
  width: 100%; /* Expand the underline to full width on hover */
}

.profile-preview {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-left: 5px;
}

#main-component {
  background-color: rgb(216, 231, 247);
  height: 100vh;
  min-width: 100vw;
  box-sizing: border-box;
}
</style>
