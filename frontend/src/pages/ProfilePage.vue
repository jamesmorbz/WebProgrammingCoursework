<template>
  <div class="header">
      <h1>{{ title }}</h1>
      <p id="smallText">Date Joined: {{ userData.date_joined }}</p>
    </div>
    <div class="profile-pictures-container">
      <div class="profile-pictures">
        <div v-for="(picture, index) in profilePictures" :key="index" @click="selectProfilePicture(index)"
             :class="{ 'selected': index === formData.profile_picture }">
          <img :src="picture" alt="Profile Picture" class="profile-picture" />
        </div>
      </div>
    </div>
  <div class="profile-page">
    
    <form class="profile-form">
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <label for="profile-edit-username" class="form-label">Username</label>
          <input type="text" class="form-control" id="profile-edit-username" v-model="formData.username"
            placeholder="Please enter a username" required :class="{ 'is-invalid': !isUsernameValid }" />
          <div v-if="!isUsernameValid" class="invalid-feedback">Invalid username (minimum 2 characters)</div>
        </div>
        <div class="col-md-6">
          <label for="profile-edit-full-name" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="profile-edit-full-name" v-model="fullName" disabled />
        </div>
      </div>
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <label for="profile-edit-first-name" class="form-label">First Name</label>
          <input type="text" class="form-control" id="profile-edit-first_name" v-model="formData.first_name"
            placeholder="Please enter your first name" required :class="{ 'is-invalid': !isFirstNameValid }" />
          <div v-if="!isFirstNameValid" class="invalid-feedback">Invalid first name (minimum 2 characters)</div>
        </div>
        <div class="col-md-6">
          <label for="profile-edit-last-name" class="form-label">Last Name</label>
          <input type="text" class="form-control" id="profile-edit-last-name" v-model="formData.last_name"
            placeholder="Please enter your last name" required :class="{ 'is-invalid': !isLastNameValid }" />
          <div v-if="!isLastNameValid" class="invalid-feedback">Invalid last name (minimum 2 characters)</div>
        </div>
      </div>
      <div class="row g-3 mb-3">
        <div class="col-md-6">
          <label for="profile-edit-email" class="form-label">Email</label>
          <input type="email" class="form-control" id="profile-edit-email" placeholder="Please enter your email address"
            v-model="formData.email" required :class="{ 'is-invalid': !isEmailValid }" />
          <div v-if="!isEmailValid" class="invalid-feedback">Invalid email address</div>
        </div>
        <div class="col-md-6">
          <label for="profile-edit-dob" class="form-label">Date of Birth</label>
          <input type="date" class="form-control" id="profile-edit-dob" v-model="formData.date_of_birth" />
        </div>
      </div>
      <div class="mb-3">
        <label for="profile-edit-dob" class="form-label">Categories</label>
        <div v-for="(item, index) in categories" :key="item">
          <CustomCheckbox :category="item" :isChecked="formData.favourite_categories.includes(item)"
            @checkbox="updateFavourites(index)" />
        </div>
      </div>
      <div class="row g-2 mb-2">
        <button type="submit" class="btn btn-primary" @click.prevent="submitForm">Update Profile</button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import CustomCheckbox from '@/components/CustomCheckbox.vue'
import profilePic1 from '@/assets/profilepic1.jpeg'
import profilePic2 from '@/assets/profilepic2.jpeg'
import profilePic3 from '@/assets/profilepic3.jpeg'
import profilePic4 from '@/assets/profilepic4.jpeg'
import profilePic5 from '@/assets/profilepic5.jpeg'
import profilePic6 from '@/assets/profilepic6.jpeg'
import profilePic7 from '@/assets/profilepic7.jpeg'
import profilePic8 from '@/assets/profilepic8.jpeg'
import profilePic9 from '@/assets/profilepic9.jpeg'
import profilePic10 from '@/assets/profilepic10.jpeg'
import profilePic11 from '@/assets/profilepic11.jpeg'
import profilePic12 from '@/assets/profilepic12.jpeg'
import profilePic13 from '@/assets/profilepic13.jpeg'
import profilePic14 from '@/assets/profilepic14.jpeg'
import profilePic15 from '@/assets/profilepic15.jpeg'
import { useProfileStore } from '@/stores/profile';
// interface Profile {
//   first_name: string,
//   last_name: string,
//   email: string,
//   date_of_birth: string,
//   date_joined: string,
//   username: string,
//   favourite_categories: string[],
//   profile_picture: typeof testImage,
// }
interface Post {
  id: number
  headline: string
  content: string
  author: string
  category: string
  date: string
}

export default defineComponent({
  components: {
    CustomCheckbox,
  },
  data() {
    return {
      title: 'Profile Page',
      isUsernameValid: true,
      isEmailValid: true,
      isFirstNameValid: true,
      isLastNameValid: true,
      userData: useProfileStore().userData,
      formData: {
        username: 'DEFAULT',
        email: 'DEFAULT',
        date_of_birth: '',
        first_name: 'DEFAULT',
        last_name: 'DEFAULT',
        favourite_categories: ['Finance'] as string[],
        profile_picture: -1,
      },
      categories: ['Finance', 'Politics', 'Sport', 'Health'],
        profilePictures: [
        profilePic1,
        profilePic2,
        profilePic3,
        profilePic4,
        profilePic5,
        profilePic6,
        profilePic7,
        profilePic8,
        profilePic9,
        profilePic10,
        profilePic11,
        profilePic12,
        profilePic13,
        profilePic14,
        profilePic15,
      ],
      articles: [] as Post[],
    }
  },
  computed: {
    fullName() {
      return `${this.userData.first_name} ${this.userData.last_name}`
    },
    // formattedDOB() {
    //   // Convert date to to "YYYY-MM-DD" format ?? depends how stored in db
    //   const [year, month, day] = this.userData.dob.split('/')
    //   return `${year}-${month}-${day}`
    // },
  },
  created() {
    console.log('Just checking what is in the pinia store')
    console.log(this.userData)
    this.fetchArticles()
    this.populateForm()
  },
  methods: {
    selectProfilePicture(index: any) {
      this.formData.profile_picture = index;
    },
    populateForm() {
      console.log(this.userData.username)
      this.formData.username = this.userData.username
      this.formData.first_name = this.userData.first_name
      this.formData.last_name = this.userData.last_name
      this.formData.email = this.userData.email
      this.formData.date_of_birth = this.userData.date_of_birth
      this.formData.favourite_categories = this.userData.favourite_categories ? this.userData.favourite_categories: this.formData.favourite_categories
      this.formData.profile_picture = this.userData.profile_picture ? this.userData.profile_picture : -1
    },
    uniqueCategories() {
      this.categories = Array.from(
        new Set(this.articles.map((article) => article.category)),
      ) // Extract unique category values from articles
    },
    fetchArticles() {
      fetch('http://localhost:8000/api/articles/')
        .then((response) => response.json())
        .then((data) => {
          this.articles = data
          this.uniqueCategories()
        })
        .catch((error) => {
          console.error('Error:', error)
        })
    },
    updateFavourites(index: number) {
      const category = this.categories[index];

      // Check if the category is already in formData.categories
      const categoryIndex = this.formData.favourite_categories.indexOf(category);

      if (categoryIndex !== -1) {
        // If found, remove it
        this.formData.favourite_categories.splice(categoryIndex, 1);
      } else {
        // If not found, add it
        this.formData.favourite_categories.push(category);
      }
    },
    submitForm() {
      // Handle form submission, you can send the formData to the server
      if (this.isFormValid()) {
        // Handle form submission
        fetch('http://localhost:8000/api/profile/', {
          method: 'POST',
          body: JSON.stringify(this.formData),
          credentials: 'include',
        }).then((response) => { console.log(response); });
      } else {
        console.log('Form validation failed');
      }
    },
    isFormValid() {
      // Add additional validation conditions as needed
      this.isUsernameValid = this.formData.username.length >= 2;
      this.isFirstNameValid = this.formData.first_name.length >= 2;
      this.isLastNameValid = this.formData.last_name.length >= 2;
      this.isEmailValid = this.isValidEmail(this.formData.email);
      // Return true if all validations pass
      return this.isUsernameValid && this.isEmailValid;
    },
    isValidEmail(email: string) {
      // Add your email validation logic here
      const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
      return emailRegex.test(email);
    },
  },
})
</script>

<style scoped>
#profile-image-prev {
  width: 150px;
  margin-bottom: 15px;
}

.profile-pictures-container {
  display: flex;
  justify-content: center; /* Center items horizontally */
}

.profile-pictures {
  display: grid;
  grid-template-columns: repeat(5, 1fr); /* 5 columns */
  gap: 10px; /* Adjust the gap between pictures */
  justify-content: center; /* Center items horizontally */
}

.profile-picture {
  width: 100px;
  height: 100px;
  cursor: pointer;
}

.selected {
    outline: 2px solid blue; /* You can customize the outline color and style */
  }

.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.profile-form {
  display: grid;
  grid-gap: 10px;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  /* Center items horizontally */
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  margin-top: 5px;
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

.image-center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* Center items vertically */
  align-items: center;
  /* Center items horizontally */
}

.justify-content-center {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>