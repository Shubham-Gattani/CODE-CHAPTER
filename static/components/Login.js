// export default {
//   template: `
//     <div class="container mt-5" style="max-width: 400px;">
//       <h3 class="text-center mb-4">SPOC LOGIN</h3>
//       <div class="form-group mb-3">
//         <label>Email:</label>
//         <input type="email" v-model="email" class="form-control" required>
//       </div>
//       <div class="form-group mb-3">
//         <label>Password:</label>
//         <input type="password" v-model="password" class="form-control" required>
//       </div>
//       <button class="btn btn-primary w-100" @click="loginUser">Submit Details</button>

//       <div v-if="errorMsg" class="alert alert-danger mt-3">
//         {{ errorMsg }}
//       </div>
//     </div>
//   `,
//   data() {
//     return {
//       email: "",
//       password: "",
//       errorMsg: ""
//     };
//   },
//   methods: {
//     async loginUser() {
//       this.errorMsg = "";

//       try {
//         const res = await fetch("/api/login", {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json"
//           },
//           body: JSON.stringify({
//             email: this.email,
//             password: this.password
//           })
//         });

//         const data = await res.json();

//         if (!res.ok) {
//           this.errorMsg = data.message || "Login failed";
//         } else {
//           // localStorage.setItem("auth_token", data.auth_token);
//           // localStorage.setItem("user_role", data.role);

//           if (data.role === "spoc") {
//             console.log("Login success:", data);
//             localStorage.setItem("user", JSON.stringify(data));
            
//             // Emit login event to parent component
//             this.$emit("login");
            
//             this.$router.push("/spoc_home"); // Go to SPOC dashboard IFF role is "spoc"
//           } else {
//             alert("Only SPOCs are allowed to login at this time");
//             setTimeout(() => {
//               this.$router.push("/");
//             }, 2000);
//           }
//         }

//       } catch (err) {
//         console.error("Login Error:", err);
//         this.errorMsg = "Server Error";
//       }
//     }
//   }
// };

export default {
  template: `
    <div class="container mt-5" style="max-width: 400px;">
      <h3 class="text-center mb-4">SPOC LOGIN</h3>
      <div v-if="step === 1">
        <div class="form-group mb-3">
          <label>Email:</label>
          <input type="email" v-model="email" class="form-control" required>
        </div>
        <button class="btn btn-primary w-100" @click="sendOtp">Send OTP</button>
      </div>
      <div v-else>
        <div class="form-group mb-3">
          <label>OTP:</label>
          <input type="text" v-model="otp" class="form-control" required>
        </div>
        <button class="btn btn-success w-100" @click="verifyOtp">Verify OTP</button>
      </div>
      <div v-if="errorMsg" class="alert alert-danger mt-3">
        {{ errorMsg }}
      </div>
    </div>
  `,
  data() {
    return {
      email: "",
      otp: "",
      errorMsg: "",
      step: 1
    };
  },
  methods: {
    async sendOtp() {
      this.errorMsg = "";
      try {
        const res = await fetch("/api/send_otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email })
        });
        const data = await res.json();
        if (!res.ok) {
          this.errorMsg = data.message || "Failed to send OTP";
        } else {
          this.step = 2;
        }
      } catch (err) {
        this.errorMsg = "Server Error";
      }
    },
    async verifyOtp() {
      this.errorMsg = "";
      try {
        const res = await fetch("/api/verify_otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, otp: this.otp })
        });
        const data = await res.json();
        if (!res.ok) {
          this.errorMsg = data.message || "OTP verification failed";
        } else {
          localStorage.setItem("user", JSON.stringify(data));
          this.$emit("login");
          this.$router.push("/spoc_home");
        }
      } catch (err) {
        this.errorMsg = "Server Error";
      }
    }
  }
};