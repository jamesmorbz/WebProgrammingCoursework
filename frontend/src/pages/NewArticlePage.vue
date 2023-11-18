<template>
  <div class="create-article-page">
    <div class="header">
      <h1>Create New Article</h1>
    </div>

    <form @submit.prevent="submitArticle" class="article-form">
      <label for="title">Title:</label>
      <input v-model="newArticle.headline" type="text" id="headline" required />

      <label for="author">Author:</label>
      <input v-model="newArticle.author" type="text" id="author" required />

      <label for="category">Category:</label>
      <input v-model="newArticle.category" type="text" id="category" required />

      <label for="content">Content:</label>
      <textarea v-model="newArticle.content" id="content" required></textarea>

      <p>
        Current Word Count: {{ currentWordCount }} - Character Count:
        {{ currentCharacterCount }}
      </p>

      <button type="submit">Create Article</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      newArticle: {
        headline: '',
        author: '',
        category: '',
        content: '',
      },
    }
  },
  computed: {
    currentWordCount() {
      return this.newArticle.content.split(' ').filter((word) => word !== '')
        .length
    },
    currentCharacterCount() {
      return this.newArticle.content.length
    },
  },
  methods: {
    submitArticle() {
      fetch('http://localhost:8000/api/articles/', {
        method: 'POST',
        body: JSON.stringify(this.newArticle),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
        })
        .catch((error) => {
          console.error('Error:', error)
        })

      console.log('New article submitted:', this.newArticle)
      this.$router.push('/') // redirects you back to the main page
    },
  },
})
</script>

<style scoped>
.create-article-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.article-form {
  display: grid;
  grid-gap: 10px;
}

label {
  font-weight: bold;
}

button {
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
