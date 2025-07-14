// Import components
import Navbar from "./components/Navbar.js";
import Footer from "./components/Footer.js";
import Login from "./components/Login.js";

// Main Pages
import Home from "./components/spoc_components/Home.js";
import StudentDetails from "./components/spoc_components/StudentDetails.js";
import Announcements from "./components/spoc_components/Announcements.js";
import Contact from "./components/spoc_components/Contact.js";
import More from "./components/spoc_components/More.js";
import landing_page from "./components/landing_page.js";

// Define routes
const routes = [
    {path: "/", component: landing_page},
    { path: "/login", component: Login },
    { path: "/spoc_home", component: Home },
    { path: "/student-details", component: StudentDetails },
    { path: "/announcements", component: Announcements },
    { path: "/contact", component: Contact },
    { path: "/more", component: More },
    { path: "*", redirect: "/spoc_home" }  // fallback to home
];

// Create Vue Router instance
const router = new VueRouter({
  mode: "hash", // or "history" if backend supports it; # DID NOT UNDERSTAND THIS. 
  routes
});

// Create main Vue instance
const app = new Vue({
  el: "#app",
  router,
  components: {
    "nav-bar": Navbar,
    "footer-component": Footer
  },
  template: `
    <div class="container">
      <nav-bar></nav-bar>
      <router-view></router-view>
      <footer-component></footer-component>
    </div>
  `
});
