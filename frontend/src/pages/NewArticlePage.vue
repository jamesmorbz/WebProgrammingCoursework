<template>
    <div class="create-article-page">
        <div class="header">
            <h1>Create New Article</h1>
        </div>

        <form @submit.prevent="submitArticle" class="article-form">
            <label for="title">Title:</label>
            <input v-model="newArticle.title" type="text" id="title" required />

            <label for="author">Author:</label>
            <input v-model="newArticle.author" type="text" id="author" required />

            <label for="category">Category:</label>
            <input v-model="newArticle.category" type="text" id="category" required />

            <label for="content">Content:</label>
            <textarea v-model="newArticle.content" id="content" required></textarea>

            <button type="submit">Create Article</button>
        </form>
    </div>
</template>
  
<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    data() {
        return {
            newArticle: {
                title: "",
                author: "",
                category: "",
                content: "",
            },
        };
    },
    methods: {
        submitArticle() {
            console.log("New article submitted:", this.newArticle);
            this.newArticle = {
                title: "",
                author: "",
                category: "",
                content: "",
            };
        },
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
  