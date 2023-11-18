<template>
    <div class="container mt-5">
        <div>
            <h2 class="mb-3">{{ article.headline }}</h2>
            <p><strong>Author:</strong> {{ article.author }}</p>
            <p><strong>Category:</strong> {{ article.category }}</p>
            <p><strong>Date:</strong> {{ formatDate(article.date) }}</p>
            <p class="mb-4">{{ article.content }}</p>

            <div class="comments-section">
                <h3 class="mb-3">Comments</h3>
                <ul class="list-unstyled">
                    <li v-for="comment in comments" :key="comment.id" class="mb-2">
                        <strong>{{ comment.user }}:</strong> {{ comment.text }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
interface Post {
    id: number;
    headline: string;
    content: string;
    author: string;
    category: string;
    date: string;
}

export default {
    props: {
        id: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            article: {} as Post,
            comments: [
                { id: 1, user: 'Alice', text: 'Great article!' },
                { id: 2, user: 'Bob', text: 'I learned a lot from this.' },
            ],
        };
    },
    created() {
        this.fetchElements();
    },
    methods: {
        formatDate(dateString: any) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
        fetchElements() {
            fetch(`http://localhost:8000/api/articles/${this.id}/`)
                .then(response => response.json())
                .then(data => {
                    this.article = data;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
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

.container {
    max-width: 800px;
}

.mb-2 {
    margin-bottom: 0.5rem !important;
}

.mb-3 {
    margin-bottom: 1rem !important;
}

.mb-4 {
    margin-bottom: 1.5rem !important;
}
</style>
  