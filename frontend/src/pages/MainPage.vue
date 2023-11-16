<template>
  <div class="main-blog-page">
    <div class="header">
      <h1>{{ title }}</h1>
      <div class="category-buttons">
        <button @click="toggleUserFavorites" :class="{ 'selected': showUserFavorites }">
          User Favorites
        </button>
        <button
          v-for="category in uniqueCategories"
          :key="category"
          @click="toggleCategoryFilter(category)"
          :class="{ 'selected': isCategoryFiltered(category) }"
        >
          {{ category }}
        </button>
        
      </div>
    </div>

    <router-link
      v-for="article in filteredArticles"
      :key="article.id"
      :to="{ name: 'Article', params: { id: article.id }}"
      class="blog-article-link"
    >
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
      selectedCategories: [] as string[], // Selected categories for filtering
      showUserFavorites: true, // Flag to show user favorites
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
      userFavorites: ["Technology", "Health"], // Example user favorites
    };
  },
  computed: {
    uniqueCategories() {
      return Array.from(new Set(this.articles.map(article => article.category))); // Extract unique category values from articles
    },
    filteredArticles() {
      let articles = this.articles.filter(article => this.selectedCategories.includes(article.category));
      if (this.showUserFavorites) {
        let favourites = this.articles.filter(article => this.userFavorites.includes(article.category)); // Show articles that match user favorites
        return Array.from(new Set(favourites.concat(articles)));
      }

      if (this.selectedCategories.length === 0) {
        return this.articles; // No categories selected, show all articles
      }

      return articles;
    },
  },
  components: {
    BlogArticle,
  },
  methods: {
    toggleCategoryFilter(category: string) {
      const index = this.selectedCategories.indexOf(category);

      if (index === -1) {
        this.selectedCategories.push(category);
      } else {
        this.selectedCategories.splice(index, 1);
      }
    },
    isCategoryFiltered(category: string) {
      return this.selectedCategories.includes(category);
    },
    toggleUserFavorites() {
      this.showUserFavorites = !this.showUserFavorites;
    },
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

.category-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.category-buttons button {
  margin: 0 5px;
  padding: 8px;
  cursor: pointer;
  border: none;
  border-radius: 20px;
  transition: background-color 0.3s ease;
}

.category-buttons button:hover {
  background-color: #f0f0f0;
}

.category-buttons button.selected {
  background-color: #007BFF;
  color: #fff;
}

.blog-article-link {
  text-decoration: none;
  color: inherit;
}

.blog-article-link:hover {
  background-color: #f0f0f0;
}
</style>
