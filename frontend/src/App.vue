<template>
  <main class="container pt-4" id="main-component">
    <div :key=count class="navbar">
      <router-link @click=increment class="nav-link" :to="{ name: 'MainPage' }">
        <i class="fas fa-home"></i> Main Page
      </router-link>
      <router-link @click=increment class="nav-link" :to="{ name: 'NewArticle' }">
        New Article
      </router-link>
      <div class="search-bar">
        <input v-model="searchQuery" type="text" placeholder="Search articles..." @keyup.enter="performSearch" />
      </div>
      <router-link @click=increment class="nav-link" :to="{ name: 'ProfilePage' }">
        <i class="fas fa-user-circle"></i> Profile Page
        <img class="profile-preview" :key=count :src=currentUserAvatar alt="Profile Preview" />
      </router-link>
      <a class="nav-link" href="http://localhost:8000/logout">Logout</a>
    </div>
    <RouterView class="flex-shrink-0" />
  </main>
</template>

<script lang="ts">
import { useProfileStore } from '@/stores/profile';
import { defineComponent } from 'vue'
import { RouterView } from 'vue-router'
import profilePic1 from '@/assets/profilepic1.jpeg'
import profilePic2 from '@/assets/profilepic2.jpeg'
import profilePic3 from '@/assets/profilepic3.jpeg'
import profilePic4 from '@/assets/profilepic4.jpeg'
import profilePic5 from '@/assets/profilepic5.jpeg'
import profilePic6 from '@/assets/profilepic6.jpeg'
import profilePic7 from '@/assets/profilepic7.jpeg'
import profilePic8 from '@/assets/profilepic8.jpeg'
import profilePic9 from '@/assets/profilepic9.jpeg'
import profilePic10 from '@/assets/profilepic10.jpeg'
import profilePic11 from '@/assets/profilepic11.jpeg'
import profilePic12 from '@/assets/profilepic12.jpeg'
import profilePic13 from '@/assets/profilepic13.jpeg'
import profilePic14 from '@/assets/profilepic14.jpeg'
import profilePic15 from '@/assets/profilepic15.jpeg'
import defaultAvatar from '@/assets/default-avatar-icon.jpg'

export default defineComponent({
  components: { RouterView },
  data() {
    return {
      currentUser: useProfileStore().userData,
      searchQuery: '',
      userAvatars: {
        0: profilePic1,
        1: profilePic2,
        2: profilePic3,
        3: profilePic4,
        4: profilePic5,
        5: profilePic6,
        6: profilePic7,
        7: profilePic8,
        8: profilePic9,
        9: profilePic10,
        10: profilePic11,
        11: profilePic12,
        12: profilePic13,
        13: profilePic14,
        14: profilePic15,
      } as any,
      currentUserAvatar: defaultAvatar,
      count: 0 as any,
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
    getUserAvatar() {
        if (this.currentUser.profile_picture in this.userAvatars) {
          this.currentUserAvatar = this.userAvatars[this.currentUser.profile_picture]
        } else {
          this.currentUserAvatar = defaultAvatar
        }
    },
    increment() {
      this.count +=1 
      console.log(this.count)
    }
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
