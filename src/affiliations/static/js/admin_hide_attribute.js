function hideAffilandEpID() {
    const affilIDField = document.querySelector(".form-row.field-affiliation_id");
    affilIDField.style.display = "none";

    const EpIDField = document.querySelector(".form-row.field-expert_panel_id");
    EpIDField.style.display = "none";
}
function toggleAffilID(value) {
    const affilIDWrapper = document.querySelector(".form-row.field-sib_affil_id_choices");
    if (value === "sibling") {
        affilIDWrapper.style.display = "block";
    } else {
        affilIDWrapper.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const affilRadioChoiceOne = document.querySelector('input[id="id_affil_id_type_choice_0"]');
    if (affilRadioChoiceOne) {
        affilRadioChoiceOne.addEventListener("click", function() {
            toggleAffilID(this.value); })    
    }

    const affilRadioChoiceTwo = document.querySelector('input[id="id_affil_id_type_choice_1"]');
    if (affilRadioChoiceTwo) {
        affilRadioChoiceTwo.addEventListener("click", function() {
            toggleAffilID(this.value); })    
    }

    if (affilRadioChoiceOne.checked) {
        toggleAffilID(affilRadioChoiceOne.value);
    } else {
        toggleAffilID(affilRadioChoiceTwo.value);
    }

    hideAffilandEpID();
});
