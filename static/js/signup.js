const ENDPOINT = API + "/api/signup"; // login API

// When client submit form login
document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  // get data from client
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  let email = document.getElementById("email").value;
  try {
    await fetch(ENDPOINT, {
      method: "POST",
      body: JSON.stringify({
        username,
        password,
        email,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data.status) throw new Error(data.message);
        // login success => save token to localStorage
        localStorage.setItem("token", data.token);
        Toast(data.message, (state = "Correct"));
        //redirect to main page
        redirect("/api/profile", 1000);
      });
  } catch (error) {
    // Error => clear all data login, focus username input
    document.getElementById("email").focus();
    document.getElementById("email").value = "";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    // message error
    Toast(error.message);
  }
});
