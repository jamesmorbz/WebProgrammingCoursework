<template>
  <div class="blog-article">
    <h2>{{ article.title }}</h2>
    <p class="meta">
      <span class="author">By {{ article.author }}</span>
      <span class="category">{{ article.category }}</span>
      <span class="date">{{ formatDate(article.date) }}</span>
    </p>
    <p>{{ article.content }}</p>
  </div>
</template>

<script>
export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.blog-article {
  margin-bottom: 20px;
  border: 2px solid #333; /* Adjust thickness as needed */
  border-radius: 10px; /* Adjust the border radius for rounded corners */
  padding: 10px;
}

.meta {
  color: #888;
  font-size: 0.8em;
}

.author {
  margin-right: 10px;
}

.category {
  margin-right: 10px;
}

.date {
  margin-right: 10px;
}
</style>
