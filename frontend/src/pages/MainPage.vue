<template>
  <div class="main-blog-page">
    <div class="header">
      <h1>{{ title }}</h1>
    </div>

    <router-link v-for="article in articles" :key="article.id" :to="{ name: 'Article', params: { id: article.id } }"
      class="blog-article-link">
      <BlogArticle :article="article" />
    </router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import BlogArticle from "@/components/BlogArticle.vue";

export default defineComponent({
  data() {
    return {
      title: "Main Page",
      articles: [
        {
          id: 1,
          title: "Sample Article 1",
          content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
          author: "John Doe",
          category: "Technology",
          date: "2023-11-16",
        },
        {
          id: 2,
          title: "Sample Article 2",
          content: "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
          author: "Jane Smith",
          category: "Science",
          date: "2023-11-15",
        },
        {
          id: 3,
          title: "Sample Article 3",
          content: "Nullam malesuada erat ut turpis. Suspendisse urna nisi, bibendum vel porttitor vel, efficitur ut tellus.",
          author: "Mark Johnson",
          category: "Health",
          date: "2023-11-14",
        },
      ],
    };
  },
  components: {
    BlogArticle,
  },
});
</script>

<style scoped>
.main-blog-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.blog-article-link {
  text-decoration: none;
  color: inherit;
}

.blog-article-link:hover {
  background-color: #f0f0f0;
}
</style>
