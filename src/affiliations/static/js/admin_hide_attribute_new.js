function hideAffilID() {
  const affilID = document.querySelector(".form-row.field-affiliation_id");
  affilID.style.display = "none";
}

function hideExpertPanelID() {
  const epID = document.querySelector(".form-row.field-expert_panel_id");
  epID.style.display = "none";
}

function toggleCDWG(value) {
  const cdwgWrapper = document.querySelector(
    ".form-row.field-clinical_domain_working_group",
  );
  if (value === "SC_VCEP" || value === "INDEPENDENT_CURATION") {
    cdwgWrapper.style.display = "none";
  } else {
    cdwgWrapper.style.display = "block";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const typeDropdown = document.querySelector("#id_type");
  if (typeDropdown) {
    typeDropdown.addEventListener("change", () => {
      toggleCDWG(typeDropdown.value);
    });
  }
  hideAffilID();
  hideExpertPanelID();
});
