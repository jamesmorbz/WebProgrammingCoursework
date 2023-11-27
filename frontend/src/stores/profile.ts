import { defineStore } from 'pinia'

interface Profile {
  first_name: string,
  last_name: string,
  email: string,
  date_of_birth: string,
  date_joined: string,
  username: string,
  favourite_categories: string[],
  profile_picture: string,
}

export const useProfileStore = defineStore('global', {
  state: () => {
    return { userData: {} as Profile }
  },
  getters: {
    getData: (state) => state.userData,
  },
  actions: {
    refresh() {
        fetch(`http://localhost:8000/api/profile/`,
            { credentials: 'same-origin',
            headers: {
                "sessionid": "mll56vo4kin7h00qckjzvblb9fhc5c64",
              } }
          )
          .then((response) => response.json())
          .then((data: any) => {
            this.userData = data
            console.log("I've just refresh the pinia state with new profile data")
            console.log(this.userData)
          })
          .catch((error) => {
            console.error('Error:', error)
          })
    },
  },
})