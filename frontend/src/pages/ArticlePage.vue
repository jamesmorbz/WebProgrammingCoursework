<template>
    <div>
      <h2>{{ article.title }}</h2>
      <p>Author: {{ article.author }}</p>
      <p>Category: {{ article.category }}</p>
      <p>Date: {{ formatDate(article.date) }}</p>
      <p>{{ article.content }}</p>
  
      <div class="comments-section">
        <h3>Comments</h3>
        <ul>
          <li v-for="comment in comments" :key="comment.id">
            <strong>{{ comment.user }}</strong>: {{ comment.text }}
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  export default {
    data() {
      return {
        article: {
          title: 'Sample Article',
          author: 'John Doe',
          category: 'Technology',
          date: '2023-11-16',
          content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
        },
        comments: [
          { id: 1, user: 'Alice', text: 'Great article!' },
          { id: 2, user: 'Bob', text: 'I learned a lot from this.' },
        ],
      };
    },
    methods: {
      formatDate(dateString: any) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
      },
    },
  };
  </script>
  
  <style scoped>
  .comments-section {
    margin-top: 20px;
  }
  
  .comments-section ul {
    list-style-type: none;
    padding: 0;
  }
  
  .comments-section li {
    margin-bottom: 10px;
  }
  </style>
  