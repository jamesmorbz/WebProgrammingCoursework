<template>
  <div class="flex-shrink-0">
    <div id="header">
      <div class="h3">
        Profile Page
      </div>
      <p id="smallText"> Date Joined: {{ userData.dateJoined }} </p>
    </div>
    <div id="body">
      <form>
        <div class="row g-3 mb-3">
          <div class="col-md-2">
            <div class="d-flex align-items-start">
              <img v-if="formData.updatedAvatar" :src="formData.updatedAvatar" class="rounded"
                alt="Preview of uploaded image" id="profile-image-prev">
              <img v-else :src="userData.profileAvatar ? userData.profileAvatar : defaultAvatar" class="rounded"
                alt="Default Image" id="profile-image-prev">
            </div>
          </div>
        </div>
        <div class="row g-3 mb-3">
          <div class=" col-md-12">
            <label for="profile-edit-image" class="form-label">Profile Image</label>
            <div class="input-group">
              <input class="form-control" type="file" id="formFile" accept="image/*" @change="handleFileChange">
              <button class="btn btn-outline-secondary" type="button" id="button-remove"
                @click="removeUpdatedImage">Remove</button>
            </div>
          </div>
        </div>
        <div class="row g-3  mb-3">
          <div class="col-md-6">
            <label for="profile-edit-username" class="form-label">Username</label>
            <input type="text" class="form-control" id="profile-edit-username" :value="userData.username">
          </div>
          <div class="col-md-6">
            <label for="profile-edit-full-name" class="form-label">Full Name</label>
            <input type="text" class="form-control" id="profile-edit-full-name" :value="fullName" disabled>
          </div>
        </div>
        <div class="row g-3  mb-3">
          <div class="col-md-6">
            <label for="profile-edit-email" class="form-label">Email</label>
            <input type="email" class="form-control" id="profile-edit-email" placeholder="Please enter your email address"
              :value="userData.email">
          </div>
          <div class="col-md-6">
            <label for="profile-edit-dob" class="form-label">Date of Birth</label>
            <input type="date" class="form-control" id="profile-edit-dob" :value="formattedDOB">
          </div>
        </div>
        <div class="mb-3">
          <label for="profile-edit-dob" class="form-label">Categories</label>
          <div v-for="item in categories" :key="item">
            <CustomCheckbox :category="item" :isChecked="userData.categories.includes(item)" />
          </div>
        </div>
      </form>
      <button type="submit" class="btn btn-primary" @click="submitForm">Update Profile</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import defaultAvatar from "../assets/default-avatar-icon.jpg";
import CustomCheckbox from "../components/CustomCheckbox.vue";
import testImage from "../assets/test-avatar.jpg";

export default defineComponent({
  components: {
    CustomCheckbox
  },
  data() {
    return {
      title: "Profile Page",
      formData: {
        username: "",
        email: "",
        dob: "",
        categories: [] as string[],
        updatedAvatar: "",
      },
      userData: {
        firstName: "John",
        lastName: "Doe",
        email: "temp@hotmail.com",
        dob: "2002/12/23",
        dateJoined: "2023/01/23",
        username: "John1",
        categories: ["Finance", "Sport", "Health"],
        //logic for loading image from backend ??
        profileAvatar: testImage,
      },
      categories: ["Finance", "Politics", "Sport", "Health"],
      defaultAvatar: defaultAvatar,
    };
  },
  computed: {
    fullName() {
      return `${this.userData.firstName} ${this.userData.lastName}`;
    },
    formattedDOB() {
      // Convert date to to "YYYY-MM-DD" format ?? depends how stored in db
      const [year, month, day] = this.userData.dob.split('/');
      return `${year}-${month}-${day}`;
    }
  },
  mounted() {
  },
  methods: {
    handleFileChange(event: Event) {
      const input = event.target as HTMLInputElement;
      const file = input.files?.[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.formData.updatedAvatar = e.target?.result as string;
        };
        reader.readAsDataURL(file);
      } else {
        input.value = "";
        this.formData.updatedAvatar = "";
        alert("Please select a valid image file.");
      }
    },
    removeUpdatedImage(event: Event) {
      const input = event.target as HTMLInputElement;
      input.value = "";
      this.formData.updatedAvatar = "";
    },
    submitForm() {
      // Handle form submission, you can send the formData to the server
      console.log("Form submitted:", this.formData, this.userData);
    },
  }
});
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