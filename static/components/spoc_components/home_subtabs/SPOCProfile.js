export default {
  data() {
    return {
      spoc: null,
      errorMsg: ""
    };
  },
  async mounted() {
    try {
      const user = JSON.parse(localStorage.getItem("user"));
      const token = user && user.auth_token;
      if (!token) {
        this.errorMsg = "No authentication token found.";
        return;
      }
      const res = await fetch("/api/spoc_dashboard/spoc_details", {
        headers: {
          "Authentication-Token": token
        }
      });
      const data = await res.json();
      if (!res.ok) {
        this.errorMsg = data.error || "Failed to fetch SPOC details.";
      } else {
        this.spoc = data;
      }
    } catch (err) {
      this.errorMsg = "Error fetching SPOC details.";
      console.error(err);
    }
  },
  template: `
    <div>
      <h4>SPOC PROFILE</h4>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-else-if="spoc">
        <p><strong>SPOC Name:</strong> {{ spoc.name }}</p>
        <p><strong>Designation:</strong> {{ spoc.designation }}</p>
        <p><strong>Contact Number:</strong> {{ spoc.contact_number }}</p>
        <p><strong>Email:</strong> {{ spoc.personal_email }}</p>
        <p><strong>Official Email:</strong> {{ spoc.user_email }}</p>
        <p><strong>College name:</strong> {{ spoc.college_name }}</p>
      </div>
      <div v-else>
        <p>Loading SPOC details...</p>
      </div>
    </div>
  `
}