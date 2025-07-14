import CollegeProfile from "./home_subtabs/CollegeProfile.js";
import SPOCProfile from "./home_subtabs/SPOCProfile.js";
import RequestLetter from "./home_subtabs/RequestLetter.js";
import MoU from "./home_subtabs/MoU.js";

export default {
  template: `
    <div>
      <h3 class="text-center my-3">MANAGE COLLEGE & SPOC DETAILS</h3>
      
      <div class="nav nav-tabs mb-3">
        <a class="nav-item nav-link" 
           :class="{ active: activeTab === 'CollegeProfile' }"
           href="#" 
           @click.prevent="activeTab = 'CollegeProfile'">College_Profile</a>
        <a class="nav-item nav-link" 
           :class="{ active: activeTab === 'SPOCProfile' }"
           href="#" 
           @click.prevent="activeTab = 'SPOCProfile'">SPOC_Profile</a>
        <a class="nav-item nav-link" 
           :class="{ active: activeTab === 'RequestLetter' }"
           href="#" 
           @click.prevent="activeTab = 'RequestLetter'">Request_Letter</a>
        <a class="nav-item nav-link" 
           :class="{ active: activeTab === 'MoU' }"
           href="#" 
           @click.prevent="activeTab = 'MoU'">MoU</a>
      </div>

      <component :is="activeTabComponent" />
    </div>
  `,
  data() {
    return {
      activeTab: 'CollegeProfile'
    }
  },
  computed: {
    activeTabComponent() {
      return this.activeTab;
    }
  },
  components: {
    CollegeProfile,
    SPOCProfile,
    RequestLetter,
    MoU
  }
};
