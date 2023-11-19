<template>
  <div class="flex-shrink-0">
    <div id="header">
      <div class="h3">{{ title }}</div>
      <p id="smallText">Date Joined: {{ userData.dateJoined }}</p>
    </div>
    <div id="body">
      <form>
        <div class="row g-3 mb-3">
          <div class="col-md-2">
            <div class="d-flex align-items-start">
              <img v-if="formData.updatedAvatar" :src="formData.updatedAvatar" class="rounded"
                alt="Preview of uploaded image" id="profile-image-prev" />
              <img v-else :src="formData.updatedAvatar" class="rounded" alt="Default Image" id="profile-image-prev" />
            </div>
          </div>
        </div>
        <div class="row g-3 mb-3">
          <div class="col-md-12">
            <label for="profile-edit-image" class="form-label">Profile Image</label>
            <div class="input-group">
              <input class="form-control" type="file" id="formFile" accept="image/*" @change="handleFileChange" />
              <button class="btn btn-outline-secondary" type="button" id="button-remove" @click="removeUpdatedImage">
                Remove
              </button>
            </div>
          </div>
        </div>
        <div class="row g-3 mb-3">
          <div class="col-md-6">
            <label for="profile-edit-username" class="form-label">Username</label>
            <input type="text" class="form-control" id="profile-edit-username" v-model="formData.username"
              placeholder="Please enter a username" required :class="{ 'is-invalid': !isUsernameValid }" />
            <div v-if="!isUsernameValid" class="invalid-feedback">Invalid username</div>
          </div>
          <div class="col-md-6">
            <label for="profile-edit-full-name" class="form-label">Full Name</label>
            <input type="text" class="form-control" id="profile-edit-full-name" v-model="fullName" disabled />
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
            <input type="date" class="form-control" id="profile-edit-dob" v-model="formData.dob" />
          </div>
        </div>
        <div class="mb-3">
          <label for="profile-edit-dob" class="form-label">Categories</label>
          <div v-for="(item, index) in categories" :key="item">
            <CustomCheckbox :category="item" :isChecked="formData.categories.includes(item)"
              @checkbox="updateFavourites(index)" />
          </div>
        </div>
      </form>
      <button type="submit" class="btn btn-primary" @click="submitForm">
        Update Profile
      </button>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent } from 'vue'
import defaultAvatar from '../assets/default-avatar-icon.jpg'
import CustomCheckbox from '../components/CustomCheckbox.vue'
import testImage from '../assets/test-avatar.jpg'

export default defineComponent({
  components: {
    CustomCheckbox,
  },
  data() {
    return {
      title: 'Profile Page',
      isUsernameValid: true,
      isEmailValid: true,
      userData: {
        firstName: 'John',
        lastName: 'Doe',
        email: 'temp@hotmail.com',
        dob: '2002-12-23',
        dateJoined: '2023-01-23',
        username: 'John1',
        categories: ['Finance', 'Sport', 'Health'],
        //logic for loading image from backend ??
        profileAvatar: testImage,
      },
      formData: {
        username: '',
        email: '',
        dob: '',
        categories: [] as string[],
        updatedAvatar: '',
      },
      categories: ['Finance', 'Politics', 'Sport', 'Health'],
      defaultAvatar: defaultAvatar,
    }
  },
  computed: {
    fullName() {
      return `${this.userData.firstName} ${this.userData.lastName}`
    },
    // formattedDOB() {
    //   // Convert date to to "YYYY-MM-DD" format ?? depends how stored in db
    //   const [year, month, day] = this.userData.dob.split('/')
    //   return `${year}-${month}-${day}`
    // },
  },
  mounted() {
    this.formData.username = this.userData.username
    this.formData.email = this.userData.email
    this.formData.dob = this.userData.dob
    this.formData.categories = this.userData.categories
    this.formData.updatedAvatar = this.userData.profileAvatar ? this.userData.profileAvatar : defaultAvatar
  },
  methods: {
    handleFileChange(event: Event) {
      const input = event.target as HTMLInputElement
      const file = input.files?.[0]
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.formData.updatedAvatar = e.target?.result as string
        }
        reader.readAsDataURL(file)
      } else {
        input.value = ''
        this.formData.updatedAvatar = ''
        alert('Please select a valid image file.')
      }
    },
    removeUpdatedImage(event: Event) {
      const input = event.target as HTMLInputElement
      input.value = ''
      this.formData.updatedAvatar = defaultAvatar
    },
    updateFavourites(index: number) {
      const category = this.categories[index];

      // Check if the category is already in formData.categories
      const categoryIndex = this.formData.categories.indexOf(category);

      if (categoryIndex !== -1) {
        // If found, remove it
        this.formData.categories.splice(categoryIndex, 1);
      } else {
        // If not found, add it
        this.formData.categories.push(category);
      }
    },
    async getUserData() {
      try {
        const response = await fetch('getuserprofileurl', {
          method: 'GET',
        });
        if (response.ok) {
          const data = await response.json();
          this.userData = data
        }
      } catch (error) {
        console.log('Error fetching user profile', error);
      }
    },
    async submitForm() {
      // Handle form submission, you can send the formData to the server
      if (this.isFormValid()) {
        // Handle form submission
        const response = await fetch('updateuserprofileurl', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            body: JSON.stringify(this.formData)
          }
        });
        if (response.ok) {
          this.userData = {
            ...this.userData,
            username: this.formData.username,
            email: this.formData.email,
            dob: this.formData.dob,
            categories: this.formData.categories,
            profileAvatar: this.formData.updatedAvatar,
          };
          console.log('Form submitted:', this.formData);
        }
        else {
          console.log('Something wrong with submitting form:', response.status, response.statusText);
        }
      } else {
        console.log('Form validation failed');
      }
    },
    isFormValid() {
      // Add additional validation conditions as needed
      this.isUsernameValid = this.formData.username.length >= 2;
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
}

#header {
  margin-top: 30px;
  margin-bottom: 50px;
}

#smallText {
  color: gray;
  font-size: 14px;
}
</style>
