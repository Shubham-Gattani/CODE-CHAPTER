export default {
  props: ['loggedIn'],
  template: `
    <div class="row border">
      <div class="col-10 fs-2 border">CODE CHAPTER</div>
      <div class="col-2 border">
        <div class="mt-1">
          <router-link v-if="!loggedIn" class="btn btn-primary my-2" to="/login">Login</router-link>
          <button v-if="loggedIn" @click="logoutUser" class="btn btn-danger">Logout</button>
        </div>
      </div>
    </div>
  `,
  methods: {
    logoutUser() {
      localStorage.clear();
      this.$emit("logout");
      this.$router.push("/");
    }
  }
}
