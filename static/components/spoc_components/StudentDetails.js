export default {
  template: `
    <div>
      <h4>STUDENT DETAILS</h4>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-else-if="students.length">
        <table class="table table-striped table-bordered">
          <thead class="thead-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Personal Email</th>
              <th scope="col">Contact Number</th>
              <th scope="col">College ID</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(student, index) in students" :key="student.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ student.name }}</td>
              <td>{{ student.personal_email }}</td>
              <td>{{ student.contact_number || 'N/A' }}</td>
              <td>{{ student.college_id }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Loading student details...</p>
      </div>
    </div>
  `,
  data() {
    return {
      students: [],
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
      const res = await fetch("/api/spoc_dashboard/student_details", {
        headers: {
          "Authentication-Token": token
        }
      });
      const data = await res.json();
      if (!res.ok) {
        this.errorMsg = data.error || "Failed to fetch student details.";
      } else {
        this.students = data.students || [];
      }
    } catch (err) {
      this.errorMsg = "Error fetching student details.";
      console.error(err);
    }
  }
}
