export default {
    template: `
    <div>
      <h4>COLLEGE PROFILE</h4>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-else-if="college">
        <p><strong>College Name:</strong> {{ college.name }}</p>
        <p><strong>Address:</strong> {{ college.address }}</p>
        <p><strong>City:</strong> {{ college.city }}</p>
        <p><strong>State:</strong> {{ college.state }}</p>
        <p><strong>PIN CODE:</strong> {{ college.pincode }}</p>
        <p><strong>ID:</strong> {{ college.id }}</p>
      </div>
      <div v-else>
        <p>Loading college details...</p>
      </div>
    </div>
  `,
  data() {
    return {
      college: null,
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
      const res = await fetch("/api/spoc_dashboard/college_details", {
        headers: {
          "Authentication-Token": token
        }
      });
      const data = await res.json();
      if (!res.ok) {
        this.errorMsg = data.error || "Failed to fetch college details.";
      } else {
        this.college = data;
      }
    } catch (err) {
      this.errorMsg = "Error fetching college details.";
      console.error(err);
    }
  },

}