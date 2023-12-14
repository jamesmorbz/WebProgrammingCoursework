<template>
  <div class="create-article-page">
    <div class="header">
      <h1> {{ title }}</h1>
    </div>
    <form class="article-form">
      <div class="form-group">
        <label for="headline">Headline:</label>
        <input v-model="newArticle.headline" type="text" id="headline" required placeholder="Please enter a headline"
          :class="{ 'is-invalid': !isHeadlineValid }" />
        <div v-if="!isHeadlineValid" class="invalid-feedback">Invalid headline (minimum 10 characters)</div>
      </div>
      <div class="form-group">
        <label for="category">Category:</label>
        <input v-model="newArticle.category" type="text" id="category" required
          placeholder="Please enter relevant categories" :class="{ 'is-invalid': !isCategoryValid }" />
        <div v-if="!isCategoryValid" class="invalid-feedback">Invalid category (minimum 2 characters)</div>
      </div>
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea v-model="newArticle.content" id="content" required placeholder="Please enter your content"
          :class="{ 'is-invalid': !isContentValid }"></textarea>
        <div v-if="!isContentValid" class="invalid-feedback">Invalid content (minimum 10 characters)</div>
      </div>
      <div class="row g-2 mb-2">
        <p>
          Current Word Count: {{ currentWordCount }} | Character Count: {{ currentCharacterCount }}
        </p>
      </div>
      <div class="row g-2 mb-2 ">
        <button type="submit" class="btn btn-primary" @click.prevent="submitArticle">Create Article</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  data() {
    return {
      isHeadlineValid: true,
      isCategoryValid: true,
      isContentValid: true,
      title: "Create New Article",
      newArticle: {
        headline: '',
        category: '',
        content: '',
      },
    };
  },
  computed: {
    currentWordCount() {
      return this.newArticle.content.split(' ').filter((word) => word !== '').length;
    },
    currentCharacterCount() {
      return this.newArticle.content.length;
    },
  },
  methods: {
    submitArticle() {
      if (this.isFormValid()) {
        // Your fetch logic
        console.log('New article submitted:', this.newArticle);
        fetch('/api/articles/', {
          method: 'POST',
          body: JSON.stringify(this.newArticle),
          credentials: 'include',
        }).then((response) => { console.log(response); });
        this.$router.push('/'); // redirects you back to the main page
      }
    },
    isFormValid() {
      // Add additional validation conditions as needed
      this.isHeadlineValid = this.newArticle.headline.length >= 10;
      this.isCategoryValid = this.newArticle.category.length >= 2;
      this.isContentValid = this.newArticle.content.length >= 10;
      // Return true if all validations pass
      return this.isHeadlineValid && this.isCategoryValid && this.isContentValid;
    },
    sleep(ms: any) {
        return new Promise(resolve => setTimeout(resolve, ms));
}

  },
});
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

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input,
textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  min-height: 40px;
}

.is-invalid {
  border-color: red;
}

.invalid-feedback {
  color: red;
  margin-top: 5px;
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
