export default {
  template: `
    <div class="container my-4">
      <h2 class="mb-3">Announcements</h2>
      <div class="embed-responsive embed-responsive-4by3 mb-3" style="height: 600px;">
        <iframe
          src="https://docs.google.com/document/d/1FeJwoJNSpzDjn4DP5NBDEJ4BIole3jnNy23FTlqRn4A/preview"
          width="100%"
          height="100%"
          frameborder="0"
          allowfullscreen>
        </iframe>
      </div>
      <button
        class="btn btn-primary"
        @click="openInNewTab"
      >
        Open in New Tab
      </button>
    </div>
  `,
  methods: {
    openInNewTab() {
      window.open("https://docs.google.com/document/d/1FeJwoJNSpzDjn4DP5NBDEJ4BIole3jnNy23FTlqRn4A", "_blank");
    }
  }
}
