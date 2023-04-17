const ENDPOINT = API + "/api/login"; // login API

chkToken();

// When client submit form login
document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  // get data from client
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;
  try {
    await fetch(ENDPOINT, {
      method: "POST",
      body: JSON.stringify({
        username: username,
        password: password,
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
    document.getElementById("username").focus();
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    // message error
    Toast(error.message);
  }
});
