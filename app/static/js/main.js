document.getElementById('diagnosisForm').addEventListener('submit', function(e) {
      //progress overlay
      const overlay = document.getElementById('progressOverlay');
      overlay.classList.add('active');
      
      // Simulate progress
      let progress = 0;
      const progressBar = document.getElementById('progressBarFill');
      const progressPercentage = document.getElementById('progressPercentage');
      const progressStatus = document.getElementById('progressStatus');
      
      const stages = [
         { percent: 20, text: 'Collecting symptoms data' },
         { percent: 40, text: 'Running AI analysis' },
         { percent: 60, text: 'Comparing with medical database' },
         { percent: 80, text: 'Generating diagnosis' },
         { percent: 95, text: 'Finalizing results' }
      ];
      
      let currentStage = 0;
      
      const interval = setInterval(() => {
         if (currentStage < stages.length) {
            progress = stages[currentStage].percent;
            progressBar.style.width = progress + '%';
            progressPercentage.textContent = progress + '%';
            progressStatus.innerHTML = stages[currentStage].text + '<span class="loading-dots"><span>.</span><span>.</span><span>.</span></span>';
            currentStage++;
         } else {
            clearInterval(interval);
         }
      }, 600);
      
      
   });

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
   anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
         target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
         });
      }
   });
});

