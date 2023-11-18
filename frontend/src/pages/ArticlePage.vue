<template>
  <div :key="reloadKey" class="container mt-5">
    <div>
      <h2 class="mb-3">{{ article.headline }}</h2>
      <p><strong>Author:</strong> {{ article.author }}</p>
      <p><strong>Word Count:</strong> {{ word_count }}</p>
      <p v-if="reading_time <= 1">
        <strong>Reading Time:</strong> {{ reading_time }} min
      </p>
      <p v-if="reading_time > 1">
        <strong>Reading Time:</strong> {{ reading_time }} mins
      </p>
      <p><strong>Category:</strong> {{ article.category }}</p>
      <p><strong>Date:</strong> {{ formatDate(article.date) }}</p>
      <p class="mb-4">{{ article.content }}</p>

      <div :key="reloadKey" class="comments-section">
        <h3 class="mb-3">Comments</h3>
        <ul class="list-unstyled">
          <li v-for="comment in comments" :key="comment.id" class="mb-2">
            <strong>{{ comment.author }}:</strong> {{ comment.content }} <br>
            Posted: {{ comment.date_time_posted }} <br>
            Last Updated: {{ comment.date_time_edited }}
            <button v-if="comment.author==currentUser" @click="deleteComment(comment.id)" class="btn btn-danger">Delete</button>
          </li>
        </ul>
      </div>

      <!-- Edit Post button to open the modal -->
      <button
        @click="openEditModal"
        class="btn btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#editModal"
      >
        Edit Post
      </button>

      <!-- Edit Modal -->
      <div
        class="modal fade"
        id="editModal"
        tabindex="-1"
        aria-labelledby="editModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="editModalLabel">Edit Article</h1>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="editPost" class="my-4">
                <div class="form-group">
                  <label for="editHeadline">Edit Headline:</label>
                  <input
                    type="text"
                    v-model="editedArticle.headline"
                    id="editHeadline"
                    required
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label for="editCategory">Edit Category:</label>
                  <input
                    type="text"
                    v-model="editedArticle.category"
                    id="editCategory"
                    required
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label for="editContent">Edit Content:</label>
                  <textarea
                    v-model="editedArticle.content"
                    id="editContent"
                    required
                    class="form-control"
                  ></textarea>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button
                type="submit"
                @click="editPost"
                data-bs-dismiss="modal"
                class="btn btn-primary"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>

      <button
        class="btn btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#newCommentModal"
      >
        New Comment
      </button>

      <div
        class="modal fade"
        id="newCommentModal"
        tabindex="-1"
        aria-labelledby="newCommentModalLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="newCommentModalLabel">New Comment</h1>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="newComment" class="my-4">
                <div class="form-group">
                  <label for="author">Author:</label>
                  <input
                    type="text"
                    v-model="newCommentData.author"
                    id="author"
                    required
                    class="form-control"
                  />
                </div>
                <div class="form-group">
                  <label for="comment">Comment:</label>
                  <textarea
                    v-model="newCommentData.content"
                    id="comment"
                    required
                    class="form-control"
                  ></textarea>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Close
              </button>
              <button
                type="submit"
                @click="newComment"
                data-bs-dismiss="modal"
                class="btn btn-primary"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
interface Post {
  id: number
  headline: string
  content: string
  author: string
  category: string
  date: string
}

interface Comments {
  id: number
  author: string
  date_time_posted: string
  date_time_edited: string
  content: string
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
      comments: [] as Comments[],
      word_count: 0,
      reading_time: 0,
      editedArticle: {} as Post,
      newCommentData: {} as Comments,
      reloadKey: 0,
      currentUser: "morbz1"
    }
  },
  created() {
    this.fetchArticle()
    this.fetchComments()
    
  },
  watch: {
    id: function () {
      console.log('ID HAS CHANGED WE NEED TO RERENDER NOW!')
      this.reloadData()
    },
  },
  methods: {
    reloadData() {
      this.reloadKey += 1
      this.fetchArticle()
      this.fetchComments()
      this.newCommentData = {} as Comments
    },
    formatDate(dateString: any) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateString).toLocaleDateString(undefined, options)
    },
    fetchArticle() {
      fetch(`http://localhost:8000/api/articles/${this.id}/`)
        .then((response) => response.json())
        .then((data) => {
          this.article = data
          this.wordCount()
          this.readingTime()
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    fetchComments() {
      fetch(`http://localhost:8000/api/articles/${this.id}/comments/`)
        .then((response) => response.json())
        .then((data) => {
          this.comments = data
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    deleteComment(comment_id: Number) {
      fetch(`http://localhost:8000/api/comments/${comment_id}/`,
      {method: 'DELETE'})
        .then((response) => response.json())
        .then((data: any) => {
          console.log(data)
          this.reloadData()
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    wordCount() {
      this.word_count = this.article.content.split(' ').length
    },
    readingTime() {
      let wordsPerMinute = 100
      this.reading_time = Math.ceil(this.word_count / wordsPerMinute)
    },
    openEditModal() {
      // Initialize the editedContent with the current content
      this.editedArticle = { ...this.article }
    },
    editPost() {
      fetch(`http://localhost:8000/api/articles/${this.id}/`, {
        method: 'PUT',
        body: JSON.stringify(this.editedArticle),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          this.reloadData()
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    newComment() {
      fetch(`http://localhost:8000/api/articles/${this.id}/comments/`, {
        method: 'POST',
        body: JSON.stringify(this.newCommentData),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          this.reloadData()
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
  },
}
</script>

<style scoped>
/* Style for the modal */
.modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
}

/* Style for the modal content */
.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

/* Style for the close button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
