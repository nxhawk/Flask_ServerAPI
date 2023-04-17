//-------------------Define constant variable----------------
const API = location.protocol + "//" + document.domain + ":" + location.port;

//------------------------------------------------------------

//---------------Toast message------------------
const Toast = (message, state = "Error", TextColor = "rgb (0, 0, 0)") => {
  Toastify({
    text: message,
    offset: {
      x: 80,
      y: 20,
    },
    duration: 3000,
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    style: {
      background:
        state == "Error"
          ? "linear-gradient(to right, rgb(255, 95, 109), rgb(255, 195, 113))"
          : "linear-gradient(to right, #00b09b, #96c93d)",
      color: TextColor,
    },
    onClick: function () {}, // Callback after click
  }).showToast();
};
//---------------------------------------

//------------------------------Redirect-------------------------
const redirect = (href, time = 0) => {
  setTimeout(() => {
    window.location.href = href;
  }, time);
};
//---------------------------------------------------------------

//-------------------check token ------------------------------
const chkToken = async () => {
  try {
    await fetch(API + "/api/getprofile", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("token"),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data || data.status == false) throw new Error();
        window.location.href = "/api/profile";
      });
  } catch (error) {
    console.log(error.message);
    document.getElementById("load").style.display = "none";
    document.querySelector("main").style.display = "block";
  }
};
//---------------------------------------------------------------
