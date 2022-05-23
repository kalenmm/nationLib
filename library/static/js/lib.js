$(document).ready(function(){
  $(".fa-search").click(function(){
    $(".wrap, .input, .searchCriteries").toggleClass("active");
    $("input[type='text']").focus();
  });
});



var btn1 = document.getElementById("darkTheme");
var btn2 = document.getElementById("whiteTheme");
let lightTheme = "../static/css/white.css";
let darkTheme = "../static/css/black.css";

var link = document.getElementById("theme-link");

btn1.addEventListener("click", function () { ChangeThemeToDark(); });
btn2.addEventListener("click", function () { ChangeThemeToWhite(); });

function ChangeThemeToDark()
{
    document.querySelector("link[class=theme]").setAttribute("href", darkTheme);

    Save(theme);
}

function ChangeThemeToWhite()
{
    document.querySelector("link[class=theme]").setAttribute("href", lightTheme);

    Save(theme);
};