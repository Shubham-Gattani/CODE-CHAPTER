export default {
  template: `
    <div>
      <h4>STUDENT DETAILS</h4>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-else-if="students.length">
        <table class="table table-bordered table-hover table-sm">
          <thead class="thead-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Personal Email</th>
              <th scope="col">Contact Number</th>
              <th scope="col">Date of Birth</th>
              <th scope="col">College Name</th>
              <th scope="col">Profile Photo</th>
              <th scope="col">ID Card</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(student, index) in students" :key="student.id">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ student.name }}</td>
              <td>{{ student.personal_email }}</td>
              <td>{{ student.contact_number || 'N/A' }}</td>
              <td>{{ student.dob || 'N/A' }}</td>
              <td>{{ student.college_name || 'N/A' }}</td>
              <td>
                <img :src="student.profile_photo" alt="Profile" v-if="student.profile_photo" width="50" height="50"/>
                <span v-else>N/A</span>
              </td>
              <td>
                <img :src="student.id_card" alt="ID Card" v-if="student.id_card" width="50" height="50"/>
                <span v-else>N/A</span>
              </td>
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
