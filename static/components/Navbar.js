export default {
  props: ['loggedIn'],
  template: `
  <div>
    <!-- TOP HEADER -->
    <div style="background-color: #001f4d; padding: 20px 0; width: 100%; position: relative;">
        <!-- Increased padding for taller header -->
        <div style="text-align: center;">
            <span
                style="font-weight: bold; color: white; font-size: 34px; display: inline-flex; align-items: center; justify-content: center; gap: 10px;">
                CODE CHAPTER - IIT MADRAS
                <img src="./static/images/IIT-Madras-Logo.png" alt="IITM Logo" style="width: 60px; height: auto;">
                <!-- Slightly larger logo for balance -->
            </span>
        </div>
        <div style="position: absolute; top: 20px; right: 30px;">
          <router-link
            v-if="!loggedIn"
            class="btn btn-info"
            to="/login"
            style="font-size: 18px; padding: 10px 20px;"
          >
            Login
          </router-link>
          <button
            v-if="loggedIn"
            @click="logoutUser"
            class="btn btn-danger"
            style="font-size: 18px; padding: 10px 20px;"
          >
            Logout
          </button>
        </div>
    </div>



      <!-- NAVIGATION BAR -->
<nav class="navbar navbar-expand-lg" style="background-color: #7ef1f1ff;">
  <div class="container-fluid">
    <div class="collapse navbar-collapse">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="loggedIn">
        <li class="nav-item">
          <router-link class="nav-link fw-bold text-dark" to="/spoc_home" active-class="active-tab">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link fw-bold text-dark" to="/student-details" active-class="active-tab">Student Details</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link fw-bold text-dark" to="/schedule" active-class="active-tab">Schedule</router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link fw-bold text-dark" href="https://docs.google.com/document/d/1FeJwoJNSpzDjn4DP5NBDEJ4BIole3jnNy23FTlqRn4A" target="_blank" rel="noopener noreferrer">Announcements</a>
        </li>
        <li class="nav-item">
          <router-link class="nav-link fw-bold text-dark" to="/contact" active-class="active-tab">Contact Us</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link fw-bold text-dark" to="/more" active-class="active-tab">More</router-link>
        </li>
      </ul>
    </div>
  </div>
</nav>

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
