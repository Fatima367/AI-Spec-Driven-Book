// plugins/personalization-plugin/client-modules/personalization.js
// This script handles the personalization button functionality

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Get all personalization buttons
  const buttons = document.querySelectorAll('.personalization-btn');
  const contentLevels = document.querySelectorAll('.content-level');

  console.log('Personalization script loaded. Found ' + buttons.length + ' buttons and ' + contentLevels.length + ' content levels');

  // Add click event listeners to buttons
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      const level = this.getAttribute('data-level');
      console.log('Button clicked for level: ' + level);

      // Remove active class from all buttons and content
      buttons.forEach(btn => {
        console.log('Removing active from button: ' + btn.getAttribute('data-level'));
        btn.classList.remove('active');
      });
      contentLevels.forEach(content => {
        console.log('Removing active from content: ' + content.getAttribute('data-level'));
        content.classList.remove('active');
      });

      // Add active class to clicked button
      this.classList.add('active');
      console.log('Added active to clicked button: ' + level);

      // Show the corresponding content level
      const targetContent = document.querySelector(`.content-level[data-level="${level}"]`);
      if (targetContent) {
        targetContent.classList.add('active');
        console.log('Added active to content: ' + level);
      } else {
        console.log('Target content not found for level: ' + level);
      }
    });
  });

  // Set default to beginner level if no button is already active
  setTimeout(() => {
    const beginnerBtn = document.querySelector('.personalization-btn[data-level="beginner"]');
    const activeBtn = document.querySelector('.personalization-btn.active');

    console.log('Checking for active button. Active button found: ' + !!activeBtn);

    if (beginnerBtn && !activeBtn) {
      console.log('No active button found, clicking beginner button');
      beginnerBtn.click();
    } else if (activeBtn) {
      console.log('Active button already exists: ' + activeBtn.getAttribute('data-level'));
    }
  }, 200); // Increased timeout to ensure everything is loaded
});