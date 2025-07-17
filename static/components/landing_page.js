export default {
  template: `
    <div class="position-relative" style="height: 100vh; background: #f8f9fa;">
      <!--<button 
        class="btn btn-primary position-absolute" 
        style="top: 30px; right: 40px; z-index: 10;"
        @click="$router.push('/login')"
      >-->
        LOGIN
      </button>
      <div class="d-flex flex-column align-items-center justify-content-center h-100">
        <img src="https://static.vecteezy.com/system/resources/previews/001/993/379/original/app-development-concept-illustration-free-vector.jpg" 
             alt="Landing Page image" 
             style="max-width: 300px; margin-bottom: 30px;">
        <h1 class="mb-3">Welcome to CODE CHAPTER</h1>
        <p class="lead text-center" style="max-width: 500px;">
          Students from your college, Teachers from IIT Madras
        </p>
      </div>
    </div>
  `
};