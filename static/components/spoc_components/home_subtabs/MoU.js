export default {
  data() {
    return {
      pdfPath: null,
      errorMsg: "",
      isLoading: false
    };
  },
  methods: {
    async fetch_mou() {
      this.isLoading = true;
      this.errorMsg = "";
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const token = user && user.auth_token;
        if (!token) {
          this.errorMsg = "No authentication token found.";
          this.isLoading = false;
          return;
        }

        const res = await fetch("/api/spoc_dashboard/mou", {
          headers: {
            "Authentication-Token": token
          }
        });

        const data = await res.json();
        if (!res.ok) {
          this.errorMsg = data.error || "Failed to fetch MoU.";
        } else {
          this.pdfPath = data.path;
          if (this.pdfPath) {
            window.open(this.pdfPath, "_blank");
          }
        }
      } catch (err) {
        this.errorMsg = "Error fetching MoU.";
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    }
  },
  template: `
    <div>
      <h4>MoU</h4>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>

      <button
        class="btn btn-primary"
        @click="fetch_mou"
        :disabled="isLoading"
      >
        {{ isLoading ? "Loading..." : "View MoU" }}
      </button>
    </div>
  `
}
