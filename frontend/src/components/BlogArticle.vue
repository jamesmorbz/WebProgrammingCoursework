<template>
  <div class="blog-article">
    <h2>{{ article.headline }}</h2>
    <p class="meta">
      <span class="author">By {{ article.author }}</span>
      <span class="category">{{ article.category }}</span>
      <span class="date">{{ formatDate(article.date) }}</span>
    </p>
    <p>{{ truncateContent(article.content) }}</p>
    <p v-if="article.content.length > maxContentLength">
      <i><strong>Click to continue Reading...</strong></i>
    </p>
    <button v-if="article.author == currentUser" @click="deleteArticle(article.id)"
      class="btn btn-danger m-2">Delete</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

interface Post {
  id: number
  headline: string
  content: string
  author: string
  category: string
  date: string
}

export default defineComponent({
  data() {
    return {
      maxContentLength: 150,
      currentUser: "john1"
    }
  },
  props: {
    article: {
      type: Object as () => Post, // Specify the type as Post
      required: true,
    },
  },
  methods: {
    formatDate(dateString: string | undefined): string {
      if (dateString === undefined) {
        return 'Invalid date';
      }
      const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    truncateContent(content: string): string {
      return content.length > this.maxContentLength
        ? content.substring(0, this.maxContentLength)
        : content
    },
    deleteArticle(article_id: Number) {
      fetch(`http://localhost:8000/api/articles/${article_id}/`,
        { method: 'DELETE' })
        .then((response) => response.json())
        .then((data: any) => {
          console.log(data)
          this.$emit('elementRefresh')
          this.$router.push("/") //this is a hack for now because I simply can't be fucked to fix it rn.
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
  },
})
</script>

<style scoped>
.blog-article {
  margin-bottom: 20px;
  border: 2px solid #333;
  /* Adjust thickness as needed */
  border-radius: 10px;
  /* Adjust the border radius for rounded corners */
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
