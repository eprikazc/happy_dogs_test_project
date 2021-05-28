/* globals $ */

const modalDialog = document.querySelector("#js-details-modal");
const modalTitle = modalDialog.querySelector("#js-details-title");
const modalContent = modalDialog.querySelector("#js-details-body");

document.querySelectorAll(".cell[data-details-url]").forEach(function(elem) {
  elem.addEventListener("click", dateClicked);
});

async function dateClicked(e) {
  const url = e.target.dataset.detailsUrl;
  const response = await fetch(url)
  if (response.ok) {
    const table = await response.text()
    modalTitle.innerHTML = e.target.dataset.title;
    modalContent.innerHTML = table;
    $(modalDialog).modal("show");
  }
}
