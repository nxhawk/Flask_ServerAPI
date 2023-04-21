const API =
  location.protocol +
  "//" +
  document.domain +
  ":" +
  location.port +
  "/api/getprofile";
const API2 =
  location.protocol +
  "//" +
  document.domain +
  ":" +
  location.port +
  "/api/v1/getposts";

let user;
const getProfile = async () => {
  try {
    await fetch(API, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("token"),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data || data.status == false) throw new Error();
        user = data.message;
        document.getElementById("load").style.display = "none";
        Funcmain();
      });
  } catch (error) {
    console.log(error.message);
    window.location.href = "/api/login";
  }
};

getProfile();

//----------------------After check token -------------------
// main func

async function Funcmain() {
  let main = document.querySelector("main");
  main.innerHTML += `
    <div style = "font-size:25px;">Hello <span style = "color:red;">${user.username}</span>, Your email <span style = "color:orange;">${user.email}</span></div>
    
    <button id = "logout">Logout</button>
  `;
  try {
    await fetch(API2, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("token"),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data || data.status == false) throw new Error();
        posts = data.posts;
        for (post of posts) {
          main.innerHTML += `<div><span>${post.post_name}</span> ${post.description}</div>`;
        }
      });
  } catch (error) {
    console.log(error.message);
  }
  //--------------- Button click=> logout------------------------
  document.getElementById("logout").addEventListener("click", () => {
    localStorage.clear();
    window.location.href = "/api/login";
  });
}
