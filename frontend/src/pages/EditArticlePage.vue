<template>
    <div class="edit-article-page">
        <div class="header">
            <h1>Edit Article</h1>
        </div>

        <form @submit.prevent="updateArticle" class="article-form">
            <label for="title">Title:</label>
            <input v-model="editedArticle.title" type="text" id="title" required />

            <label for="author">Author:</label>
            <input v-model="editedArticle.author" type="text" id="author" required />

            <label for="category">Category:</label>
            <input v-model="editedArticle.category" type="text" id="category" required />

            <label for="content">Content:</label>
            <textarea v-model="editedArticle.content" id="content" required></textarea>

            <button type="submit">Update Article</button>
        </form>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    data() {
        return {
            editedArticle: {
                id: 1,
                title: "Sample Article 1",
                author: "John Doe",
                category: "Technology",
                content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
            },
        };
    },
    methods: {
        updateArticle() {
            console.log("Article updated:", this.editedArticle);
            this.$router.push({ name: 'Article', params: { id: this.editedArticle.id } });
        },
    },
});
</script>
  
<style scoped>
.edit-article-page {
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
    background-color: #007BFF;
    color: #fff;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
</style>
  