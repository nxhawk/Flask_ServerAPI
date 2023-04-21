const API =
  location.protocol +
  "//" +
  document.domain +
  ":" +
  location.port +
  "/api/v1/getallposts";
const API2 =
  location.protocol +
  "//" +
  document.domain +
  ":" +
  location.port +
  "/api/v1/newpost";

let posts;
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
        posts = data.posts;
        document.getElementById("load").style.display = "none";
        Funcmain();
      });
  } catch (error) {
    console.log(error.message);
    window.location.href = "/api/login";
  }
};

getProfile();

const newPost = async () => {
  try {
    num = Math.floor(Math.random() * 1000);
    text = num.toString();
    await fetch(API2, {
      method: "POST",
      body: JSON.stringify({
        post_name: "Hello guy " + text,
        description: "Day la post " + text + " vi du thui hen",
      }),
      headers: {
        "Content-Type": "application/json",
        Authorization: localStorage.getItem("token"),
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data || data.status == false) throw new Error();
        window.location.reload();
      });
  } catch (error) {
    console.log(error.message);
  }
};
//----------------------After check token -------------------
// main func

function Funcmain() {
  let main = document.querySelector("main");
  // sort posts follow time update (to show new post(create/update))
  posts.sort(function (a, b) {
    return parseFloat(b.updated_time) - parseFloat(a.updated_time);
  });

  //show information all posts
  for (post of posts) {
    main.innerHTML += `<div>${post.post_name} ${post.author} ${post.updated_time}</div>`;
  }

  document.getElementById("newPost").addEventListener("click", () => {
    newPost();
  });

  //--------------------------------END-----------------
}
