function hideAffilandEpID() {
    const affilIDField = document.querySelector(".form-row.field-affiliation_id");
    affilIDField.style.display = "none";

    const EpIDField = document.querySelector(".form-row.field-expert_panel_id");
    EpIDField.style.display = "none";
}

function toggleCDWG(value) {
    const cdwgWrapper = document.querySelector(".form-row.field-clinical_domain_working_group");
    if (value === "SC_VCEP") {
        cdwgWrapper.style.display = "none";
    } else {
        cdwgWrapper.style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const typeDropdown = document.querySelector('select[id="id_type"]');
    if (typeDropdown) {
        typeDropdown.addEventListener("change", function() {
            toggleCDWG(this.value); })    
    }

    hideAffilandEpID();
});
