export default {
  data() {
    return {
      pdfPath: null,
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

      const res = await fetch("/api/spoc_dashboard/mou", {
        headers: {
          "Authentication-Token": token
        }
      });

      const data = await res.json();
      if (!res.ok) {
        this.errorMsg = data.error || "Failed to fetch MoU PDF.";
      } else {
        this.pdfPath = data.path;
        // Load PDF.js and render the PDF
        const pdfjsLib = window['pdfjs-dist/build/pdf'];
        pdfjsLib.GlobalWorkerOptions.workerSrc = '//cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js';
        const loadingTask = pdfjsLib.getDocument(this.pdfPath);
        loadingTask.promise.then(pdf => {
          pdf.getPage(1).then(page => {
            const viewport = page.getViewport({ scale: 1.5 });
            const canvas = document.getElementById('pdf-canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            page.render({ canvasContext: context, viewport: viewport });
          });
        });
      }
    } catch (err) {
      this.errorMsg = "Error fetching MoU.";
      console.error(err);
    }
  },
  template: `
    <div>
      <h4>MoU</h4>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-if="pdfPath" id="pdf-container">
        <canvas id="pdf-canvas"></canvas>
        <a :href="pdfPath" download class="btn btn-primary mt-2">Download MoU</a>
</div>
      <div v-else>
        <p>Loading MoU PDF...</p>
      </div>
    </div>
  `
}
