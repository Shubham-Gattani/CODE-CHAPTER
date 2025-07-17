import CollegeProfile from "./home_subtabs/CollegeProfile.js";
import SPOCProfile from "./home_subtabs/SPOCProfile.js";
import MoU from "./home_subtabs/MoU.js";

export default {
  template: `
    <div class="container my-4">
  <h3 class="text-center mb-4 text-white py-2 rounded" style="background-color: rgb(0, 31, 77);;">
    MANAGE COLLEGE & SPOC DETAILS
  </h3>

  <!-- Tabs -->
  <div class="nav nav-pills justify-content-center gap-2 mb-4" role="tablist">
    <a class="nav-link"
        role="tab"
       :class="{ active: activeTab === 'CollegeProfile' }"
       @click.prevent="activeTab = 'CollegeProfile'"
       href="#">
       College Profile
    </a>
    <a class="nav-link"
        role="tab"
       :class="{ active: activeTab === 'SPOCProfile' }"
       @click.prevent="activeTab = 'SPOCProfile'"
       href="#">
       SPOC Profile
    </a>
    <a class="nav-link"
        role="tab"
       :class="{ active: activeTab === 'MoU' }"
       @click.prevent="activeTab = 'MoU'"
       href="#">
       MoU
    </a>
  </div>

  <!-- Tab Content -->
  <div class="card shadow-sm border-0 p-4">
    <component :is="activeTabComponent" />
  </div>
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
    MoU
  }
};
