const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");

const passwordField = document.querySelector("#passwordField");
const passconfirmField = document.querySelector("#passconfirmField");
const showPasswordToggle = document.querySelector("#showPasswordToggle");
const showConfirmPasswordToggle = document.querySelector("#showConfirmPasswordToggle");

const confirmPasswordToggle = document.querySelector("#confirmPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");

// Variable to keep submit button disabled if either of username or password is invalid
let usernameValid = true;
let emailValid = true;
// still incomplete


const handleToggleInput = (e) => {
  // Determine which icon was clicked (password or confirm password)
  const target = e.target;
  
  // Check if the clicked element is the password toggle icon
  if (target === showPasswordToggle) {
    const isPasswordVisible = passwordField.type === "text";
    passwordField.setAttribute("type", isPasswordVisible ? "password" : "text");
    showPasswordToggle.classList.toggle("fa-eye", isPasswordVisible);
    showPasswordToggle.classList.toggle("fa-eye-slash", !isPasswordVisible);
  }

  // Check if the clicked element is the confirm password toggle icon
  if (target === showConfirmPasswordToggle) {
    const isConfirmPasswordVisible = passconfirmField.type === "text";
    passconfirmField.setAttribute("type", isConfirmPasswordVisible ? "password" : "text");
    showConfirmPasswordToggle.classList.toggle("fa-eye", isConfirmPasswordVisible);
    showConfirmPasswordToggle.classList.toggle("fa-eye-slash", !isConfirmPasswordVisible);
  }
};

// Add event listeners for both toggle icons
if (showPasswordToggle) {
  showPasswordToggle.addEventListener("click", handleToggleInput);
}

if (showConfirmPasswordToggle) {
  showConfirmPasswordToggle.addEventListener("click", handleToggleInput);
}



// Email Validation
if (emailField){
  emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
  
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
  
    if (emailVal.length > 0) {
      fetch("/authentication/validate-email", {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.email_error) {
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            emailFeedBackArea.style.display = "block";
            emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
          } else {
            submitBtn.removeAttribute("disabled");
          }
        });
    }
  });
  

  emailField.addEventListener('keypress',(e)=>{
    if(e.key === 'Enter'){
      e.preventDefault(); // Prevent form submission
      passwordField.focus(); // Move to the password field
  }
  });

}

// Username Validation
if (usernameField){
  usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
  
    usernameSuccessOutput.style.display = "block";
  
    usernameSuccessOutput.textContent = `Checking  ${usernameVal}`;
  
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
  
    if (usernameVal.length >= 0) {
      fetch("/authentication/validate-username", {
        body: JSON.stringify({ username: usernameVal}),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          usernameSuccessOutput.style.display = "none";
          if (data.username_error) {
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display = "block";
            feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            submitBtn.disabled = true;
          } else {
            submitBtn.removeAttribute("disabled");
          }
        });
    }
  });



  // navigate to the next field by hitting the "Enter" key
usernameField.addEventListener('keypress',(e)=>{
  if(e.key === 'Enter'){
    e.preventDefault(); // Prevent form submission
    emailField.focus(); // Move to the email field
}
});

  
  
}


// function checkSubmitButtonState(){
//   if(usernameValid && emailValid){
//     submitBtn.removeAttribute("disabled");
//   }
//   else{
//     submitBtn.disabled = true;
//   }
// }