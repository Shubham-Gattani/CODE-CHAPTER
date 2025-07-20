import CollegeProfile from "./home_subtabs/CollegeProfile.js";
import SPOCProfile from "./home_subtabs/SPOCProfile.js";
import MoU from "./home_subtabs/MoU.js";

export default {
  template: `
    <div class="container my-4">
    <h3 class="text-center mb-4 text-white py-2 rounded" style="background-color: rgb(0, 31, 77);">
      MANAGE COLLEGE & SPOC DETAILS
    </h3>

    <div class="row">
      <!-- Left Sidebar Card -->
      <div class="col-md-3 mb-3" style="margin-top: 4.5rem;">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h6 class="card-title fw-bold text-secondary mb-3">Quick Links</h6>
            <ul class="list-group list-group-flush">
              <li class="list-group-item px-0 py-1">
                <a href="https://forms.gle/YOUR_GOOGLE_FORM_LINK" target="_blank" class="text-decoration-none text-primary fw-medium">
                  SPOC Profile Change Request
                </a>
              </li>
              <li class="list-group-item px-0 py-1">
                <a href="https://docs.google.com/document/d/YOUR_FAQ_DOC_LINK/export?format=doc" target="_blank" class="text-decoration-none text-primary fw-medium">
                  FAQs
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Right Main Content -->
      <div class="col-md-9">
        <!-- Tabs -->
        <div class="nav nav-pills justify-content-start gap-2 mb-4" role="tablist">
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
        <div class="card shadow-sm border-0 p-4 mb-3">
          <component :is="activeTabComponent" />
        </div>
      </div>
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
