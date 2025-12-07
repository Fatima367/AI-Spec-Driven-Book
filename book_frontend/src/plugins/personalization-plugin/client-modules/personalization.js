// plugins/personalization-plugin/client-modules/personalization.js
// This script handles the personalization button functionality

// Function to initialize personalization functionality
function initializePersonalization() {
  // Get all personalization buttons
  const buttons = document.querySelectorAll('.personalization-btn');
  const contentLevels = document.querySelectorAll('.content-level');

  if (buttons.length === 0 || contentLevels.length === 0) {
    // If elements aren't ready yet, try again after a short delay
    setTimeout(initializePersonalization, 300);
    return;
  }

  console.log('Personalization script loaded. Found ' + buttons.length + ' buttons and ' + contentLevels.length + ' content levels');

  // Add click event listeners to buttons
  buttons.forEach(button => {
    // Remove any existing listeners to avoid duplicates by cloning the button
    const newButton = button.cloneNode(true);
    button.parentNode.replaceChild(newButton, button);

    newButton.addEventListener('click', function() {
      const level = this.getAttribute('data-level');
      console.log('Button clicked for level: ' + level);

      // Remove active class from all buttons and content
      document.querySelectorAll('.personalization-btn').forEach(btn => {
        console.log('Removing active from button: ' + btn.getAttribute('data-level'));
        btn.classList.remove('active');
      });
      document.querySelectorAll('.content-level').forEach(content => {
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
  const beginnerBtn = document.querySelector('.personalization-btn[data-level="beginner"]');
  const activeBtn = document.querySelector('.personalization-btn.active');

  console.log('Checking for active button. Active button found: ' + !!activeBtn);

  if (beginnerBtn && !activeBtn) {
    console.log('No active button found, clicking beginner button');
    beginnerBtn.click();
  } else if (activeBtn) {
    console.log('Active button already exists: ' + activeBtn.getAttribute('data-level'));
  }
}

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  initializePersonalization();
});

// Also try to initialize after a delay in case of dynamic content loading
setTimeout(initializePersonalization, 500);

// Additionally, try to handle cases where content is loaded dynamically
if (document.readyState === 'complete' || document.readyState === 'interactive') {
  setTimeout(initializePersonalization, 300);
}