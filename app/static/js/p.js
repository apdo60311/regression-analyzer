const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".menu-items .item a");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");

// sidebarClose.addEventListener("click", () => sidebar.classList.toggle("close"));

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    event.preventDefault();
    console.log("clicked");
    // Get the href attribute value of the clicked item
    const targetId = item.getAttribute("href").substring(1);

    // Hide all content sections
    document.querySelectorAll(".details").forEach((content) => {
      content.style.display = "none";
    });

    // Show the target content section
    document.getElementById(targetId).style.display = "block";
    document.getElementById(targetId).style.width = "auto";

    // menu.classList.add("submenu-active");
    // item.classList.add("show-submenu");
    // menuItems.forEach((item2, index2) => {
    //   if (index !== index2) {
    //     item2.classList.remove("show-submenu");
    //   }
    // });
  });
});

subMenuTitles.forEach((title) => {
  title.addEventListener("click", () => {
    menu.classList.remove("submenu-active");
  });
});

const dataOverview = document.getElementById("DataOverview");
const heat_map = document.getElementById("heat_map");
const corr_matrix = document.getElementById("corr_matrix");
const boxplot = document.getElementById("boxplot");

dataOverview.addEventListener("click", () => {});
dataOverview.addEventListener("click", () => {});
dataOverview.addEventListener("click", () => {});
dataOverview.addEventListener("click", () => {});
